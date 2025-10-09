from ui.display.preview_item import PreviewItem
from PySide6.QtWidgets import QLabel
from ui.display.image import PixMap

class PreviewImage(PreviewItem):
    def __init__(self, page_no:int, document_name:str, document_page_range:list = None, image:PixMap = None, curr_size:int = 100, contains:list = None):
        super().__init__(page_no, document_name, document_page_range, image, curr_size, contains)
    
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
        return PreviewImage(self.page_no, self.document_name, self.document_page_range, self.image, self.curr_size)