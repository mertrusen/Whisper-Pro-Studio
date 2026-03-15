from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox, QDoubleSpinBox, QSpinBox, QLineEdit, QTabWidget, QPushButton, QMessageBox
from PySide6.QtCore import Signal, Qt
import platform

# Import external translations
try:
    from ..translations import HELP_TEXTS, TRANSLATIONS
except ImportError:
    from translations import HELP_TEXTS, TRANSLATIONS

ALL_LANGUAGES = ["auto - Otomatik", "tr - Türkçe", "en - İngilizce"] + sorted([
    "de - Almanca", "fr - Fransızca", "es - İspanyolca", "it - İtalyanca", "ja - Japonca", 
    "ru - Rusça", "ar - Arapça", "az - Azerbaijani"
])

class SettingsFormWidget(QWidget):
    config_changed = Signal(str, object) # key, value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "tr"
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.widgets = {}
        self.labels = {}
        
        self._init_general_tab()
        self._init_format_tab()
        self._init_ai_tab()
        self._init_fine_tab()
        self._init_tech_tab()
        
        self.setup_interlocking_logic()
        self.update_language(self.current_lang)

    def _create_tab(self, title_key):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        layout.addStretch() # Push everything up
        
        self.tabs.addTab(tab, title_key) # Temporary title, will be replaced in update_language
        self.labels[f"tab_{title_key}"] = (self.tabs, self.tabs.count() - 1)
        
        return layout

    def _init_general_tab(self):
        layout = self._create_tab("gen")
        self._add_combo(layout, "model", "lbl_model", ["turbo", "large-v3", "medium", "base", "small", "tiny"], "turbo", help_key="model")
        self._add_combo(layout, "lang", "lbl_lang", ALL_LANGUAGES, "tr - Türkçe", help_key="language")
        self._add_combo(layout, "task", "lbl_task", ["transcribe", "translate"], "transcribe", help_key="task")
        default_dev = "mps" if platform.system() == "Darwin" else ("cuda" if platform.system() == "Windows" else "cpu")
        self._add_combo(layout, "device", "lbl_dev", ["mps", "cuda", "cpu"], default_dev, help_key="device")

    def _init_format_tab(self):
        layout = self._create_tab("out")
        self._add_combo(layout, "fmt", "lbl_fmt", ["srt", "vtt", "txt", "all"], "srt", help_key="output_format")
        self._add_entry(layout, "custom_name", "lbl_name", help_key="custom_filename")
        self._add_checkbox(layout, "gap_filling", "lbl_gap", False, help_key="gap_fill")
        self._add_double_spin(layout, "gap_threshold", "lbl_gap_thresh", 0.1, 10.0, 2.0)
        self._add_checkbox(layout, "word_ts", "lbl_time", True, help_key="word_timestamps")
        self._add_checkable_spin(layout, "use_lines", "max_line", "lbl_line_cnt", 1, 5, 2, True, help_key="max_line_count")
        self._add_checkable_spin(layout, "use_width", "line_width", "lbl_line_wd", 10, 100, 42, False, help_key="line_width")
        self._add_checkable_spin(layout, "use_words", "max_word", "lbl_max_w", 1, 50, 7, True, help_key="max_words_per_line")

    def _init_ai_tab(self):
        layout = self._create_tab("ai")
        self._add_entry(layout, "prompt", "lbl_prompt", help_key="initial_prompt")
        self._add_double_spin(layout, "temp", "lbl_temp", 0.0, 1.0, 0.0, 0.1, help_key="temperature")
        self._add_checkbox(layout, "condition", "lbl_ctx", True, help_key="condition")

    def _init_fine_tab(self):
        layout = self._create_tab("fine")
        self._add_double_spin(layout, "patience", "lbl_pat", 0.1, 5.0, 1.0, 0.1, help_key="patience")
        self._add_spin(layout, "beam", "lbl_beam", 1, 10, 5, help_key="beam_size")
        self._add_double_spin(layout, "no_speech", "lbl_nospeech", 0.1, 1.0, 0.6, 0.1, help_key="thresholds")

    def _init_tech_tab(self):
        layout = self._create_tab("tech")
        self._add_checkbox(layout, "fp16", "lbl_fp16", False, help_key="fp16")
        self._add_double_spin(layout, "len_pen", "lbl_lenpen", 0.1, 5.0, 1.0, 0.1, help_key="length_penalty")
        self._add_double_spin(layout, "comp", "lbl_comp", 0.1, 5.0, 2.4, 0.1, help_key="compression")

    def _create_help_btn(self, help_key):
        btn = QPushButton("?")
        btn.setFixedSize(24, 24)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("QPushButton { font-weight: bold; color: #0078d7; border-radius: 12px; border: 1px solid #0078d7; } QPushButton:hover { background-color: #0078d7; color: white; }")
        btn.clicked.connect(lambda: self._show_help(help_key))
        return btn

    def _show_help(self, help_key):
        msg = HELP_TEXTS.get(self.current_lang, HELP_TEXTS["en"]).get(help_key, "No info available.")
        QMessageBox.information(self, "Info", msg)

    def _add_combo(self, layout, key, trans_key, items, default, help_key=None):
        h = QHBoxLayout()
        lbl = QLabel()
        self.labels[trans_key] = lbl
        
        cb = QComboBox()
        cb.addItems(items)
        cb.setCurrentText(default)
        cb.currentTextChanged.connect(lambda v: self.config_changed.emit(key, v))
        
        h.addWidget(lbl)
        h.addWidget(cb)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[key] = cb

    def _add_entry(self, layout, key, trans_key, help_key=None):
        h = QHBoxLayout()
        lbl = QLabel()
        self.labels[trans_key] = lbl
        
        le = QLineEdit()
        le.textChanged.connect(lambda v: self.config_changed.emit(key, v))
        
        h.addWidget(lbl)
        h.addWidget(le)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[key] = le
        
    def _add_checkbox(self, layout, key, trans_key, default, help_key=None):
        h = QHBoxLayout()
        chk = QCheckBox()
        self.labels[trans_key] = chk
        chk.setChecked(default)
        chk.stateChanged.connect(lambda v: self.config_changed.emit(key, bool(v)))
        
        h.addWidget(chk)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        h.addStretch()
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[key] = chk

    def _add_spin(self, layout, key, trans_key, min_v, max_v, default, help_key=None):
        h = QHBoxLayout()
        lbl = QLabel()
        self.labels[trans_key] = lbl
        
        sp = QSpinBox()
        sp.setRange(min_v, max_v)
        sp.setValue(default)
        sp.valueChanged.connect(lambda v: self.config_changed.emit(key, v))
        
        h.addWidget(lbl)
        h.addWidget(sp)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[key] = sp

    def _add_double_spin(self, layout, key, trans_key, min_v, max_v, default, step=1.0, help_key=None):
        h = QHBoxLayout()
        lbl = QLabel()
        self.labels[trans_key] = lbl
        
        sp = QDoubleSpinBox()
        sp.setRange(min_v, max_v)
        sp.setValue(default)
        sp.setSingleStep(step)
        sp.valueChanged.connect(lambda v: self.config_changed.emit(key, v))
        
        h.addWidget(lbl)
        h.addWidget(sp)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[key] = sp
        
    def _add_checkable_spin(self, layout, chk_key, spin_key, trans_key, min_v, max_v, default_spin, default_chk, help_key=None):
        h = QHBoxLayout()
        chk = QCheckBox()
        self.labels[trans_key] = chk
        chk.setChecked(default_chk)
        
        sp = QSpinBox()
        sp.setRange(min_v, max_v)
        sp.setValue(default_spin)
        
        chk.stateChanged.connect(lambda v: self.config_changed.emit(chk_key, bool(v)))
        sp.valueChanged.connect(lambda v: self.config_changed.emit(spin_key, v))
        
        h.addWidget(chk)
        h.addWidget(sp)
        if help_key: h.addWidget(self._create_help_btn(help_key))
        layout.insertLayout(layout.count() - 1, h)
        self.widgets[chk_key] = chk
        self.widgets[spin_key] = sp

    def update_language(self, lang):
        self.current_lang = lang
        texts = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        
        for key, widget in self.labels.items():
            if key.startswith("tab_"):
                # Handle tab titles
                tab_widget, index = widget
                if key in texts:
                    tab_widget.setTabText(index, texts[key])
            else:
                # Handle generic labels/checkboxes
                if key in texts:
                    if isinstance(widget, QLabel):
                        widget.setText(texts[key])
                    elif isinstance(widget, QCheckBox):
                        widget.setText(texts[key])

    def setup_interlocking_logic(self):
        def _line_count_changed(state):
            if state:
                self.widgets["use_width"].setChecked(True)
                self.widgets["use_words"].setChecked(False)
                self.widgets["word_ts"].setChecked(True)
        self.widgets["use_lines"].stateChanged.connect(_line_count_changed)
        
        def _line_width_changed(state):
            if not state:
                self.widgets["use_lines"].setChecked(False)
            else:
                self.widgets["use_words"].setChecked(False)
                self.widgets["word_ts"].setChecked(True)
        self.widgets["use_width"].stateChanged.connect(_line_width_changed)
        
        def _max_words_changed(state):
            if state:
                self.widgets["use_width"].setChecked(False)
                self.widgets["use_lines"].setChecked(False)
                self.widgets["word_ts"].setChecked(True)
        self.widgets["use_words"].stateChanged.connect(_max_words_changed)

        def _device_changed(text):
            # MPS (Mac) ve FP16 (Yarım Hassasiyet) birlikte çalışınca NaN/çökme hatası veriyor.
            if text == "mps":
                if self.widgets["fp16"].isChecked():
                    self.widgets["fp16"].setChecked(False)
                    QMessageBox.warning(self, "MPS & FP16 Alert", 
                        "Whisper on Mac (MPS) is unstable with FP16 enabled and often causes crashes (NaN values).\n\n"
                        "FP16 has been disabled for stability. Please use FP32 (FP16 Off) on Apple Silicon.")
                
                # MPS (Mac) ve Word Timestamps birlikte çalışınca float64 hatası veriyor.
                if self.widgets["word_ts"].isChecked():
                    self.widgets["word_ts"].setChecked(False)
                    QMessageBox.warning(self, "MPS & Word Timestamps Alert", 
                        "Whisper's 'Word Timestamps' feature is technically incompatible with Apple GPU (MPS) acceleration because it requires high-precision math (float64).\n\n"
                        "To use Word Timestamps on Mac:\n1. Set Model to 'turbo'\n2. Set Device to 'cpu'\n\nThis will work perfectly and still be fast!")
                
                # Large-v3 + MPS uyarısı
                if self.widgets["model"].currentText() == "large-v3":
                    QMessageBox.warning(self, "MPS & Large-v3 Stability Warning", 
                        "The 'large-v3' model is known to be numerically unstable on Apple Silicon (MPS) and may crash with NaN errors even without FP16.\n\n"
                        "Recommendation: Use the 'turbo' model for much better speed/stability on Mac, or switch Device to 'cpu' if you must use large-v3.")
        self.widgets["device"].currentTextChanged.connect(_device_changed)

        def _model_changed(text):
            if text == "large-v3" and self.widgets["device"].currentText() == "mps":
                QMessageBox.warning(self, "Model Stability Warning", 
                    "You selected 'large-v3' on 'mps' device.\n\n"
                    "This combination often crashes on Mac. It is highly recommended to use the 'turbo' model or 'cpu' device for large-v3.")
        self.widgets["model"].currentTextChanged.connect(_model_changed)

        def _fp16_changed(state):
            if state and self.widgets["device"].currentText() == "mps":
                self.widgets["fp16"].setChecked(False)
                QMessageBox.warning(self, "MPS & FP16 Warning", 
                    "Enabling FP16 on Apple Silicon (MPS) device is known to cause numerical errors (NaN).\n\n"
                    "It is highly recommended to keep FP16 OFF when using 'mps'.")
        self.widgets["fp16"].stateChanged.connect(_fp16_changed)

        def _word_ts_changed(state):
            if state and self.widgets["device"].currentText() == "mps":
                self.widgets["word_ts"].setChecked(False)
                QMessageBox.warning(self, "MPS Limitation", 
                    "Word Timestamps is currently NOT compatible with Apple Silicon (MPS) acceleration.\n\n"
                    "Please use 'cpu' as device if you need word-level precision.")
        self.widgets["word_ts"].stateChanged.connect(_word_ts_changed)

    def update_values(self, config):
        for k, v in config.items():
            if k in self.widgets:
                w = self.widgets[k]
                if isinstance(w, QComboBox): w.setCurrentText(v)
                elif isinstance(w, QLineEdit): w.setText(v)
                elif isinstance(w, QCheckBox): w.setChecked(bool(v))
                elif isinstance(w, (QSpinBox, QDoubleSpinBox)): w.setValue(v)

