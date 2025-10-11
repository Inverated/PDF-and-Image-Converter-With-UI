from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class PixMap():
    def __init__(self, q_image:QImage, width, height):
        self.image = QPixmap.fromImage(q_image)
        self.width = width
        self.height = height
        self.normWidth = width
        self.normHeight = height
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def normaliseWidth(self, newWidth):
        self.normWidth = newWidth
        self.normHeight = self.height / self.width * newWidth
        
    def normaliseHeight(self, newHeight):
        self.normHeight = newHeight
        self.normWidth = self.width / self.height * newHeight
        
    def resetNorm(self):
        self.normWidth = self.width
        self.normHeight = self.height
        
    def scaled(self, size:int) -> QPixmap:
        return self.image.scaled(self.normWidth*size/100, self.normHeight*size/100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

