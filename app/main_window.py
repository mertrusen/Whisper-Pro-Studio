import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QScrollArea, QFrame, QLabel, QMessageBox,
    QInputDialog, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

from .preset_manager import PresetManager
from .backend import WhisperProcess, build_whisper_command
from .widgets.file_selection import FileSelectionWidget
from .widgets.settings_form import SettingsFormWidget
from .widgets.log_viewer import LogViewerWidget

try:
    from .translations import TRANSLATIONS
except ImportError:
    from translations import TRANSLATIONS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Whisper Pro Studio")
        self.resize(1100, 800)
        self.setMinimumSize(900, 600)
        
        self.config = {}
        self.preset_manager = PresetManager()
        self.worker = None
        self.current_lang = "tr"
        
        self.history = []
        self.history_index = -1
        self.ignore_changes = False
        
        self._init_ui()
        self._load_initial_state()
        self._update_language(self.current_lang)
        
    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 1) Top: Header & Tools
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QVBoxLayout(header_frame)
        
        top_bar = QHBoxLayout()
        self.main_title = QLabel("WHISPER PRO STUDIO")
        self.main_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0078d7;")
        
        self.btn_undo = QPushButton("⟲")
        self.btn_redo = QPushButton("⟳")
        btn_tr = QPushButton("🇹🇷")
        btn_en = QPushButton("🇬🇧")
        
        for btn in (self.btn_undo, self.btn_redo, btn_tr, btn_en):
            btn.setFixedSize(40, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
        self.btn_undo.clicked.connect(self._undo)
        self.btn_redo.clicked.connect(self._redo)
        btn_tr.clicked.connect(lambda: self._update_language("tr"))
        btn_en.clicked.connect(lambda: self._update_language("en"))
        
        self.btn_undo.setEnabled(False)
        self.btn_redo.setEnabled(False)
        
        top_bar.addWidget(self.main_title)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_undo)
        top_bar.addWidget(self.btn_redo)
        
        spacer = QLabel("|")
        spacer.setStyleSheet("color: #555; font-size: 16px; margin: 0 10px;")
        top_bar.addWidget(spacer)
        
        top_bar.addWidget(btn_tr)
        top_bar.addWidget(btn_en)
        
        header_layout.addLayout(top_bar)
        
        # File Selection Area
        self.file_widget = FileSelectionWidget()
        self.file_widget.config_changed.connect(self._on_config_changed)
        header_layout.addWidget(self.file_widget)
        
        main_layout.addWidget(header_frame)
        
        # 2) Middle: Settings
        self.settings_widget = SettingsFormWidget()
        self.settings_widget.config_changed.connect(self._on_config_changed)
        main_layout.addWidget(self.settings_widget)
        
        # Command Preview Area
        self.preview_label = QLabel("COMMAND PREVIEW:")
        self.preview_label.setStyleSheet("font-weight: bold; color: #888; margin-top: 10px;")
        main_layout.addWidget(self.preview_label)
        
        self.cmd_preview = QLabel()
        self.cmd_preview.setWordWrap(True)
        self.cmd_preview.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.cmd_preview.setStyleSheet("background-color: #1e1e1e; color: #00b0ff; padding: 10px; font-family: Consolas; border-radius: 4px;")
        main_layout.addWidget(self.cmd_preview)
        
        # 3) Presets and Actions
        action_layout = QHBoxLayout()
        
        self.btn_save_preset = QPushButton()
        self.btn_save_preset.clicked.connect(self._save_preset)
        
        self.btn_load_preset = QPushButton()
        self.btn_load_preset.clicked.connect(self._load_preset)
        
        self.btn_del_preset = QPushButton()
        self.btn_del_preset.clicked.connect(self._del_preset)
        
        action_layout.addWidget(self.btn_save_preset)
        action_layout.addWidget(self.btn_load_preset)
        action_layout.addWidget(self.btn_del_preset)
        action_layout.addStretch()
        
        self.btn_start = QPushButton()
        self.btn_start.setMinimumHeight(40)
        self.btn_start.setMinimumWidth(200)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setStyleSheet("font-weight: bold; background-color: #0078d7; color: white;")
        self.btn_start.clicked.connect(self._toggle_process)
        action_layout.addWidget(self.btn_start)
        
        main_layout.addLayout(action_layout)
        
        # 4) Log Viewer
        self.log_viewer = LogViewerWidget()
        main_layout.addWidget(self.log_viewer, stretch=1)

    def _update_language(self, lang):
        self.current_lang = lang
        texts = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        
        self.main_title.setText(texts.get("title", "WHISPER PRO STUDIO"))
        self.btn_save_preset.setText(texts.get("btn_save_pre", "Save Preset"))
        self.btn_load_preset.setText(texts.get("btn_load_pre", "Load Preset"))
        self.btn_del_preset.setText(texts.get("btn_del_pre", "Delete Preset"))
        
        if self.worker and self.worker.isRunning():
            self.btn_start.setText(texts.get("btn_stop", "STOP"))
        else:
            self.btn_start.setText(texts.get("btn_start", "START WHISPER"))
            
        self.preview_label.setText(texts.get("lbl_preview", "COMMAND PREVIEW"))
        
        # Update child widgets
        self.settings_widget.update_language(lang)
        self.file_widget.update_language(lang)
        self._update_preview()

    def _load_initial_state(self):
        saved_config = self.preset_manager.load_last_session()
        self.config.update(saved_config)
        self.file_widget.update_values(self.config)
        self.settings_widget.update_values(self.config)
        self._update_preview()
        
    def closeEvent(self, event):
        self.preset_manager.save_last_session(self.config)
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        super().closeEvent(event)
        
    def _on_config_changed(self, key, value):
        if self.ignore_changes: return
        self.config[key] = value
        self._save_state()
        self._update_preview()
        
    def _save_state(self):
        if self.ignore_changes: return
        current_state = self.config.copy()
        if self.history and self.history[self.history_index] == current_state: return
        if self.history_index < len(self.history) - 1: self.history = self.history[:self.history_index + 1]
        self.history.append(current_state)
        self.history_index += 1
        self._update_undo_redo_buttons()

    def _undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self._restore_state(self.history[self.history_index])

    def _redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._restore_state(self.history[self.history_index])

    def _restore_state(self, state):
        self.ignore_changes = True
        self.config.update(state)
        self.file_widget.update_values(self.config)
        self.settings_widget.update_values(self.config)
        self.ignore_changes = False
        self._update_preview()
        self._update_undo_redo_buttons()

    def _update_undo_redo_buttons(self):
        if hasattr(self, 'btn_undo'):
            self.btn_undo.setEnabled(self.history_index > 0)
        if hasattr(self, 'btn_redo'):
            self.btn_redo.setEnabled(self.history_index < len(self.history) - 1)

    def _update_preview(self):
        cmd = build_whisper_command(self.config)
        formatted_cmd = [f'"{x}"' if ' ' in x else x for x in cmd]
        cmd_str = " ".join(formatted_cmd)
        
        extras = []
        if self.config.get("gap_filling", False):
            extras.append(f"[AUTOMATION: Gap Filling Active (Threshold: {self.config.get('gap_threshold', 2.0)}s)]")
            
        custom_name = self.config.get("custom_name", "").strip()
        if custom_name:
            extras.append(f"[AUTOMATION: Files will be renamed to: {custom_name}]")
            
        if extras:
            cmd_str += "\n\n" + "\n".join(extras)
            
        self.cmd_preview.setText(cmd_str)

    def _save_preset(self):
        name, ok = QInputDialog.getText(self, "Save Preset", "Preset Name:")
        if ok and name:
            self.preset_manager.add_preset(name, self.config.copy())
            QMessageBox.information(self, "Success", f"Preset '{name}' saved.")
            
    def _load_preset(self):
        presets = list(self.preset_manager.presets.keys())
        if not presets:
            QMessageBox.warning(self, "Warning", "No presets available.")
            return
            
        name, ok = QInputDialog.getItem(self, "Load Preset", "Select Preset:", presets, 0, False)
        if ok and name:
            preset_config = self.preset_manager.presets[name]
            self.config.update(preset_config)
            self.file_widget.update_values(preset_config)
            self.settings_widget.update_values(preset_config)
            
    def _del_preset(self):
        presets = list(self.preset_manager.presets.keys())
        if not presets: return
        name, ok = QInputDialog.getItem(self, "Delete Preset", "Select Preset to Delete:", presets, 0, False)
        if ok and name:
            self.preset_manager.delete_preset(name)
            QMessageBox.information(self, "Deleted", f"Preset '{name}' deleted.")
            
    def _toggle_process(self):
        if self.worker and self.worker.isRunning():
            self._stop_process()
        else:
            self._start_process()
            
    def _start_process(self):
        input_file = self.config.get("file", "")
        if not input_file or not os.path.exists(input_file):
            QMessageBox.critical(self, "Error", "Please select a valid media file.")
            return
            
        out_dir = self.config.get("out_dir", "")
        if not out_dir or not os.path.exists(out_dir):
            QMessageBox.critical(self, "Error", "Please select a valid output directory.")
            return

        cmd = build_whisper_command(self.config)
        
        self.log_viewer.clear_log()
        self.log_viewer.append_log(">>> Running command:\n" + " ".join(cmd) + "\n\n")
        
        self.worker = WhisperProcess(cmd, self.config, input_file, out_dir)
        self.worker.log_signal.connect(self.log_viewer.append_log)
        self.worker.finished_signal.connect(self._on_process_finished)
        
        texts = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"])
        self.btn_start.setText(texts.get("btn_stop", "STOP PROCESS"))
        self.btn_start.setStyleSheet("font-weight: bold; background-color: #e81123; color: white;")
        
        self.worker.start()
        
    def _stop_process(self):
        if self.worker:
            self.worker.stop()
            
    def _on_process_finished(self, success, message):
        texts = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"])
        self.btn_start.setText(texts.get("btn_start", "START WHISPER"))
        self.btn_start.setStyleSheet("font-weight: bold; background-color: #0078d7; color: white;")
        
        if success:
            QMessageBox.information(self, "Finished", message)
        else:
            QMessageBox.warning(self, "Warning/Error", message)
