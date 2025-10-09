from ui.display.preview_item import PreviewItem
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag, QColor, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData

from ui.display.image import PixMap

class PreviewPdf(PreviewItem):
    def __init__(self, page_no:int, document_name:str, document_page_range:list = None, image:PixMap = None, curr_size:int = 100, contains:list = None):
        super().__init__(page_no, document_name, document_page_range, image, curr_size, contains)
        #add white background
        self.image_label.setStyleSheet("background-color: white")
        
        width = self.image_label.width()
        height = self.image_label.height()
        
        scaled_width = self.drag_width_px
        scaled_height = height/width * self.drag_width_px
        scaled_drag = self.image_label.pixmap().scaled(scaled_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bg = QPixmap(scaled_width, scaled_height)
        bg.fill(Qt.white)
        painter = QPainter(bg)
        painter.drawPixmap(0, 0, scaled_drag)
        painter.end()
        
        self.drag_image = bg
    
    def setImage(self):
        # Image (Change to preview at lower resolution from file list?)
        image_label = QLabel()
        scaled = self.image.scaled(self.curr_size)
        image_label.setPixmap(scaled)
        image_label.setFixedSize(scaled.size())
        return image_label
        
    def update_image_size(self, new_size): 
        self.curr_size = new_size
        scaled = self.image.scaled(new_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
    def copyOf(self):
        return PreviewPdf(self.page_no, self.document_name, self.document_page_range, self.image, self.curr_size)
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            drag.setPixmap(self.drag_image)
            drag.exec(Qt.DropAction.MoveAction)