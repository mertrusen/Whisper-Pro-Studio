from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PySide6.QtGui import QFont

class LogViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        lbl = QLabel("Process Log:")
        lbl.setStyleSheet("font-weight: bold; color: #888;")
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Consolas", 10))
        self.text_edit.setStyleSheet("background-color: #000; color: #0f0; border: none;")
        
        layout.addWidget(lbl)
        layout.addWidget(self.text_edit)
        
    def append_log(self, text):
        self.text_edit.moveCursor(self.text_edit.textCursor().MoveOperation.End)
        self.text_edit.insertPlainText(text)
        self.text_edit.moveCursor(self.text_edit.textCursor().MoveOperation.End)
        
    def clear_log(self):
        self.text_edit.clear()
