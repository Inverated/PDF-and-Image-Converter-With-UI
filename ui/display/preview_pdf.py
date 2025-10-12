from typing import override
from ui.display.preview_item import PreviewItem
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData

from ui.display.image import PixMap

class PreviewPdf(PreviewItem):
    def __init__(self, page_no:int, document_name:str, full_path:str, extension:str, document_page_range:list = None, image:PixMap = None, curr_size:int = 100, contains:list = None):
        super().__init__(page_no, document_name, full_path, extension, document_page_range, image, curr_size, contains)
        #add white background
        if not self.image_label.pixmap().isNull():
            self.image_label.setStyleSheet("background-color: white")
        self.drag_image = self.create_drag_image()
    
    def create_drag_image(self):
        #additional drag image with solid bg (pixmap seperate from qimage)
        bg = None
        
        qpixmap = self.image_label.pixmap()
        if not qpixmap.isNull():
            width = self.image_label.width()
            height = self.image_label.height()
            
            scaled_width = self.drag_width_px
            scaled_height = height/width * self.drag_width_px
            
            scaled_drag = qpixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            bg = QPixmap(scaled_width, scaled_height)
            bg.fill(Qt.white)
            
            painter = QPainter(bg)
            painter.drawPixmap(0, 0, scaled_drag)
            painter.end()
        return bg
    
    @override
    def setImage(self):
        image_label = QLabel()
        scaled = self.image.scaled(self.curr_size)
        if scaled != None:
            image_label.setPixmap(scaled)
            image_label.setFixedSize(scaled.size())
        return image_label
       
    @override 
    def update_image_size(self, new_size): 
        if new_size % 10 != 0:
            return
        self.curr_size = new_size
        scaled = self.image.scaled(new_size)
        if scaled != None:
            self.image_label.setPixmap(scaled)
            self.image_label.setFixedSize(scaled.size())
        
    @override
    def copyOf(self) -> 'PreviewPdf':
        return PreviewPdf(self.page_no, self.document_name, self.full_path, self.extension, self.document_page_range, self.image, self.curr_size)
    
    @override
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            if self.drag_image != None:
                mime = QMimeData()
                drag.setMimeData(mime)
                drag.setPixmap(self.drag_image)
            drag.exec(Qt.DropAction.MoveAction)