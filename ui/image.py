from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class PixMap():
    def __init__(self, path='test/download.jpg', scale:int=100):
        self.scale = 100
        self.image = QPixmap(path)
        self.width = self.image.width()
        self.height = self.image.height()
    
    def scaled(self, size:int) -> QPixmap:
        return self.image.scaled(self.width*size/100, self.height*size/100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
