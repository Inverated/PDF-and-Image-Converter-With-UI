from ui.display.image import PixMap


class Page(PixMap):
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.normWidth = width
        self.normHeight = height
        
    def scaled(self, size:int):
        return self.image
        