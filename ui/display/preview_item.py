from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyle, QPushButton, QFrame
from PySide6.QtGui import QDrag, QImage
from PySide6.QtCore import QSize, Signal, Qt, QMimeData
from ui.display.image import PixMap


class PreviewItem(QWidget):
    removeRequested = Signal(QWidget)
    def __init__(self, page_no:int, document_name:str, document_page_range:list = None, image:QImage = None, curr_size:int = 100):
        super().__init__()   
        layout = QHBoxLayout()
        
        self.page_no = page_no
        self.curr_size = curr_size
        self.document_page_range = document_page_range
        self.document_name = document_name
        self.image = image

        self.page_label = QLabel("Pg. " + str(page_no))
        
        self.image_stack = QVBoxLayout()
        
        # Visual indicator for drag and drop
        top_indicator, bottom_indicator = QFrame(), QFrame()
        top_indicator.setFrameShape(QFrame.HLine)
        top_indicator.setFrameShadow(QFrame.Sunken)
        bottom_indicator.setFrameShape(QFrame.HLine)
        bottom_indicator.setFrameShadow(QFrame.Sunken)
        top_indicator.hide()
        bottom_indicator.hide()
        
        
        # Add dash if page ranges
        image_title = str(self.document_name) + " Page "
        if self.document_page_range[0] == self.document_page_range[1]:
            image_title += str(self.document_page_range[0])
        else:
            image_title += str(self.document_page_range[0]) + ' - ' + str(self.document_page_range[1])
        self.image_title = QLabel(image_title)
        
        
        # Image (Change to preview at lower resolution from file list?)
        self.image_label = QLabel()
        self.original_image = PixMap(self.image)
        scaled = self.original_image.scaled(self.curr_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
        self.image_stack.addWidget(top_indicator)
        self.image_stack.addWidget(self.image_label, alignment=Qt.AlignHCenter)
        self.image_stack.addWidget(self.image_title, alignment=Qt.AlignHCenter)
        self.image_stack.addWidget(bottom_indicator)

        
        button = QPushButton()
        pixmap_icon = QStyle.StandardPixmap.SP_DialogDiscardButton
        icon = self.style().standardIcon(pixmap_icon)
        button.setIconSize(QSize(16, 16))
        button.setIcon(icon)
        button.clicked.connect(self.remove_clicked)


        layout.addWidget(self.page_label, stretch=0)
        layout.addLayout(self.image_stack, stretch=1)
        layout.addWidget(button, stretch=0)
                
        self.setLayout(layout)
                
    def update_page_no(self, page_no:int):
        self.page_label.setText("Pg. " + str(page_no))
        
    def update_image_size(self, new_size): 
        self.curr_size = new_size
        scaled = self.original_image.scaled(new_size)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(scaled.size())
        
    def remove_clicked(self):
        return self.removeRequested.emit(self)
    
    def compact(self, next):
        new_range = [self.document_page_range[0], next.document_page_range[1]] 
        return PreviewItem(self.page_no, self.document_name, new_range, self.image, self.curr_size)
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            #Preview drag
            drag.setPixmap(self.image_label.pixmap())
            
            drag.exec(Qt.DropAction.MoveAction)
    
    def set_top_indicator(self, show:bool):
        qline = self.image_stack.itemAt(0).widget()
        qline.show() if show else qline.hide()
    
    def set_bottom_indicator(self, show:bool):
        qline = self.image_stack.itemAt(self.image_stack.count() - 1).widget()
        qline.show() if show else qline.hide()
        
    def copyOf(self):
        return PreviewItem(self.page_no, self.document_name, self.document_page_range, self.image, self.curr_size)

