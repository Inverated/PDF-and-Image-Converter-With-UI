from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal

class OptionBar(QToolBar):
    previewRequested = Signal(bool)
    darkThemeRequested = Signal(bool)
    
    def __init__(self):
        super().__init__("")
        self.setMovable(False)
        #Reversed, will reverse when initialised
        self.preview = not True
        self.dark = not True
        
        self.preview_toggle = QAction("Preview Enabled", self)
        self.preview_toggle.setToolTip("""Change the ability to render image for preview
                                  Disable to reduce memory usage""")
        self.preview_toggle.triggered.connect(self.set_preview)
        self.addAction(self.preview_toggle)
        
        self.theme_toggle = QAction("Dark", self)
        self.theme_toggle.setToolTip("Flashbang?")
        self.theme_toggle.triggered.connect(self.set_theme)
        self.addAction(self.theme_toggle)
        
        self.set_preview(None)
        self.set_theme(None)
        
    def set_preview(self, _):
        self.preview = not self.preview
        self.previewRequested.emit(self.preview)
        
        txt = "Preview Enabled" if self.preview else "Preview Disabled"
        self.preview_toggle.setText(txt)
        
    def set_theme(self, _):
        self.dark = not self.dark
        self.darkThemeRequested.emit(self.dark)
        
        txt = "Dark" if self.dark else "Light"
        self.theme_toggle.setText(txt)
