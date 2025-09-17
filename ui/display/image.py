from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class PixMap():
    def __init__(self, q_image:QImage):
        self.image = QPixmap.fromImage(q_image)
        self.width = self.image.width()
        self.height = self.image.height()
    
    def scaled(self, size:int) -> QPixmap:
        return self.image.scaled(self.width*size/100, self.height*size/100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
