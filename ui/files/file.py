from os.path import splitext

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QImage
from PySide6.QtCore import QSize
import fitz

from ui.display.preview_item import PreviewItem


class File(QWidget):
    def __init__(self, path_name):
        super().__init__()
        self.setStyleSheet("background-color: red;")
        self.initial_page_size = 100
        
        with open(path_name, 'rb') as f:
            self.data = f.read()
        
        self.path_name = path_name
        basename, self.extension = splitext(path_name)
        self.document_name = basename.split('/')[-1]
        
        if self.extension == 'pdf':
            self.image_list: list[PreviewItem] = self.__convert_pdf_to_list()        
        else:
            self.image_list: list[PreviewItem] = self.__convert_image_to_list()
        
        self.page_count = len(self.image_list)
        #error catch if cannot read
        
        
        # Render simple display
        layout = QHBoxLayout()
        
        label = QLabel(self.file_name())
        
        remove_button = QPushButton()
        trash_pixmap = QStyle.StandardPixmap.SP_DialogDiscardButton
        trash_icon = self.style().standardIcon(trash_pixmap)
        remove_button.setIconSize(QSize(16, 16))
        remove_button.setIcon(trash_icon)
        
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(remove_button)
        self.setLayout(layout)
        
    def file_name(self):
        return "{}{}\t{} page(s)".format(self.document_name, self.extension, self.page_count)
        
    
    def __convert_image_to_list(self, ) -> list[PreviewItem]:
        page_range = [1,1]
        image = QImage(self.path_name)
        return [PreviewItem(page_no=1, document_name=self.document_name,
                            document_page_range=page_range, curr_size=self.initial_page_size,
                            image=image)]
         
    def __convert_pdf_to_list(self) -> list[PreviewItem]:
        doc = fitz.open(self.path_name)
        
        image_list: list[PreviewItem] = []
        
        for page_no in range(len(doc)):
            curr_page = page_no + 1
            page_range = [curr_page, curr_page]
            
            pixmap:fitz.Pixmap = doc.load_page(page_no).get_pixmap()
            qimg = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            
            image_list.append(PreviewItem(page_no=curr_page, document_name=self.document_name, 
                                          document_page_range=page_range, curr_size=self.initial_page_size,
                                          image=qimg))
        return image_list
            
            
        
        
        