from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyle, QPushButton, QFrame
from PySide6.QtGui import QDrag
from PySide6.QtCore import QSize, Signal, Qt, QMimeData
from ui.display.image import PixMap

class PreviewItem(QWidget):
    removeRequested = Signal(QWidget)
    downloadRequested = Signal(list)
    
    def __init__(self, page_no:int, document_name:str, full_path:str, extension:str, document_page_range:list[int] = None, image:PixMap = None, curr_size:int = 100, contains:list = None):
        super().__init__()   
        self.drag_width_px = 200
        layout = QHBoxLayout()
        self.page_no = page_no  #Page order 
        self.curr_size = curr_size
        self.document_page_range = document_page_range  #Page of original document
        self.document_name = document_name
        self.full_path = full_path
        self.image = image
        self.contains = contains
        self.extension = extension

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
        
        self.image_title = QLabel()
        self.__set_title()
        
        self.image_label:QLabel = self.setImage()
        
        self.image_stack.addWidget(top_indicator)
        if not self.image_label.pixmap().isNull():  
            self.image_stack.addWidget(self.image_label, alignment=Qt.AlignHCenter)
        self.image_stack.addWidget(self.image_title, alignment=Qt.AlignHCenter)
        self.image_stack.addWidget(bottom_indicator)

        
        discard_button = QPushButton()
        discard_icon = QStyle.StandardPixmap.SP_DialogDiscardButton
        icon = self.style().standardIcon(discard_icon)
        discard_button.setIconSize(QSize(16, 16))
        discard_button.setIcon(icon)
        discard_button.clicked.connect(self.remove_clicked)

        save_button = QPushButton()
        save_icon = QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.style().standardIcon(save_icon)
        save_button.setIconSize(QSize(16, 16))
        save_button.setIcon(icon)
        save_button.clicked.connect(self.download_clicked)

        layout.addWidget(self.page_label, stretch=0)
        layout.addLayout(self.image_stack, stretch=1)
        layout.addWidget(save_button, stretch=0)
        layout.addWidget(discard_button, stretch=0)
                
        self.setLayout(layout)
    
    def disablePreview(self):
        return self
        
    def getImage(self):
        return self.image
    
    def setImage(self):
        #Overide
        return None
        
    def update_image_size(self, new_size): 
        #Overide
        return
                  
    def update_page_no(self, page_no:int):
        self.page_label.setText("Pg. " + str(page_no))
    
    def download_clicked(self):
        self.downloadRequested.emit([self])
      
    def remove_clicked(self):
        return self.removeRequested.emit(self)
    
    def compact(self, next):
        self.document_page_range = [self.document_page_range[0], next.document_page_range[1]] 
        if self.contains == None:
            self.contains = [next]
        else:
            self.contains.append(next)
        self.__set_title()
        return self
    
    def compact_list(self, lis:list["PreviewItem"]):
        start = self.document_page_range[0]
        if len(lis) > 1:
            self.document_page_range = [start, lis[-1].document_page_range[1]]
        else:
            self.document_page_range = [start, start]
        lisCopy = [each.copyOf() for each in lis]
        self.contains = lisCopy
        self.__set_title()
        return self
    
    def uncompact(self):
        hidden_stack = self.contains
        self.contains = None
        self.document_page_range[1] = self.document_page_range[0]
        self.__set_title()
        return hidden_stack
    
    def __set_title(self):
        # Add dash if page ranges
        image_title = str(self.document_name) + " Page "
        if self.document_page_range[0] == self.document_page_range[1]:
            image_title += str(self.document_page_range[0])
        else:
            image_title += str(self.document_page_range[0]) + ' - ' + str(self.document_page_range[1])
        self.image_title.setText(image_title)
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            qpixmap = self.image_label.pixmap()
            if not qpixmap.isNull():
                #Preview drag
                width = self.image_label.width()
                height = self.image_label.height()
                
                drag.setPixmap(qpixmap.scaled(self.drag_width_px, height/width * self.drag_width_px, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            drag.exec(Qt.DropAction.MoveAction)

    def set_top_indicator(self, show:bool):
        qline = self.image_stack.itemAt(0).widget()
        qline.show() if show else qline.hide()
    
    def set_bottom_indicator(self, show:bool):
        qline = self.image_stack.itemAt(self.image_stack.count() - 1).widget()
        qline.show() if show else qline.hide()
        
    def copyOf(self) -> 'PreviewItem':
        return None

