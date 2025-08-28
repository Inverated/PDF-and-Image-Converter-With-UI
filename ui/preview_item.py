from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QSize, Signal

from ui.image import PixMap

class PreviewItem(QWidget):
    removeRequested = Signal(QWidget)
    def __init__(self, page_no:int, document_name:str = None, document_page_range:list = None, image = None, curr_size:int = 100):
        super().__init__()   
        layout = QHBoxLayout()
        
        self.page_no = page_no
        self.curr_size = curr_size
        self.document_page_range = document_page_range
        self.document_name = document_name
        self.image = image

        self.page_label = QLabel("Pg. " + str(page_no))
        
        self.image_label = QLabel()
        self.pixmap = PixMap(self.image)
        scaled = self.pixmap.scaled(self.curr_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
        button = QPushButton()
        pixmap_icon = QStyle.StandardPixmap.SP_DialogDiscardButton
        icon = self.style().standardIcon(pixmap_icon)
        button.setIconSize(QSize(16, 16))
        button.setIcon(icon)
        button.clicked.connect(self.remove_clicked)

        layout.addWidget(self.page_label)
        layout.addStretch()
        layout.addWidget(self.image_label)
        layout.addStretch()
        layout.addWidget(button)
        
        self.setLayout(layout)
    
    def update_page_no(self, page_no:int):
        self.page_label.setText("Pg. " + str(page_no))
        
    def update_image_size(self, new_size): 
        self.curr_size = new_size
        scaled = self.pixmap.scaled(new_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
    def remove_clicked(self):
        return self.removeRequested.emit(self)
    
    def compact(self, next):
        new_range = [self.document_page_range[0], next.document_page_range[1]] 
        return PreviewItem(self.page_no, self.document_name, new_range, self.image, self.curr_size)