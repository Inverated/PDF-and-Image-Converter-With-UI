from typing import override
from backend.file_downloader import Downloader
from ui.display.preview_item import PreviewItem
from PySide6.QtWidgets import QLabel, QFileDialog
from ui.display.image import PixMap

class PreviewImage(PreviewItem):
    def __init__(self, page_no:int, document_name:str, full_path:str, extension:str, document_page_range:list = None, image:PixMap = None, curr_size:int = 100, contains:list = None):
        super().__init__(page_no, document_name, full_path, extension, document_page_range, image, curr_size, contains)
    
    @override
    def setImage(self):
        # Image (Change to preview at lower resolution from file list?)
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
    def copyOf(self) -> 'PreviewImage':
        out = PreviewImage(self.page_no, self.document_name, self.full_path, self.extension, self.document_page_range, self.image, self.curr_size)
        self.deleteLater()
        return out
    
    def disablePreview(self):
        out = PreviewImage(self.page_no, self.document_name, self.full_path, self.extension, self.document_page_range, PixMap(None, self.image.getWidth(), self.image.getHeight()), self.curr_size)
        self.deleteLater()
        return out