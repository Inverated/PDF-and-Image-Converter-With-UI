from os.path import basename

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage
import fitz

from ui.preview_item import PreviewItem

class File(QWidget):
    def __init__(self, path_name):
        super().__init__()
        
        with open(path_name, 'rb') as f:
            self.data = f.read()
        
        doc = fitz.open(path_name)
        
        document_name = basename(path_name)
        image_list: list[PreviewItem] = []
        
        for page_no in range(len(doc)):
            curr_page = page_no + 1
            page_range = [curr_page, curr_page]
            default_page_size = 100
            
            pixmap:fitz.Pixmap = doc.load_page(page_no).get_pixmap()
            qimg = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            
            image_list.append(PreviewItem(page_no=curr_page, document_name=document_name, 
                                          document_page_range=page_range, curr_size=default_page_size,
                                          image=qimg))
            
            
        
        
        