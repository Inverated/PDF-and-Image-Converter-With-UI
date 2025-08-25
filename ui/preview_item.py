from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QSize, Signal

from ui.image import PixMap

class PreviewItem(QWidget):
    removeRequested = Signal(QWidget)
    def __init__(self, curr_size:int = 100, image = None, page_no = None):
        super().__init__()   
        layout = QHBoxLayout()
        
        self.page_label = QLabel("Pg. " + str(page_no))
        
        self.image_label = QLabel()
        self.pixmap = PixMap('test/download.jpg')
        scaled = self.pixmap.scaled(curr_size)
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
        scaled = self.pixmap.scaled(new_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
    def remove_clicked(self):
        return self.removeRequested.emit(self)