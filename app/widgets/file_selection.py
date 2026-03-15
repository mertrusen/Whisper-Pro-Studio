from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PySide6.QtCore import Signal
try:
    from ..translations import TRANSLATIONS
except ImportError:
    from translations import TRANSLATIONS

class FileSelectionWidget(QWidget):
    config_changed = Signal(str, str) # key, value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "tr"
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.labels = {}
        
        # File path
        file_layout = QHBoxLayout()
        self.file_label = QLabel()
        self.labels["lbl_media"] = self.file_label
        
        self.file_input = QLineEdit()
        
        self.file_btn = QPushButton()
        self.labels["btn_sel1"] = self.file_btn # Temporary key
        self.file_btn.clicked.connect(self._browse_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_btn)
        
        # Output dir
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel()
        self.labels["lbl_save"] = self.dir_label
        
        self.dir_input = QLineEdit()
        
        self.dir_btn = QPushButton()
        self.labels["btn_sel2"] = self.dir_btn
        self.dir_btn.clicked.connect(self._browse_dir)
        
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.dir_btn)
        
        layout.addLayout(file_layout)
        layout.addLayout(dir_layout)
        
        self.file_input.textChanged.connect(lambda t: self.config_changed.emit("file", t))
        self.dir_input.textChanged.connect(lambda t: self.config_changed.emit("out_dir", t))
        
        self.update_language(self.current_lang)
        
    def _browse_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", "Media Files (*.mp3 *.wav *.mp4 *.m4a *.flac *.mkv)")
        if f:
            self.file_input.setText(f)
            
    def _browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if d:
            self.dir_input.setText(d)
            
    def update_values(self, config):
        if "file" in config: self.file_input.setText(config["file"])
        if "out_dir" in config: self.dir_input.setText(config["out_dir"])

    def update_language(self, lang):
        self.current_lang = lang
        texts = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        
        if "lbl_media" in texts: self.file_label.setText(texts["lbl_media"])
        if "lbl_save" in texts: self.dir_label.setText(texts["lbl_save"])
        if "btn_sel" in texts: 
            self.file_btn.setText(texts["btn_sel"])
            self.dir_btn.setText(texts["btn_sel"])
