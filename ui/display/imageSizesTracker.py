class ImageSizes:
    def __init__(self):
        self.width = []
        self.height = []
        self.sorted = False
    
    def add_size(self, width, height):
        self.width.append(width)
        self.height.append(height)
        self.sorted = False

    def delete_size(self, width, height):
        if width in self.width:
            self.width.remove(width)
        if height in self.height:
            self.height.remove(height)
        
    def get_min(self):
        if not self.sorted:
            self.width.sort()
            self.height.sort()
            self.sorted = True
        return {
            'width': min(self.width) if self.width else None,
            'height': min(self.height) if self.height else None
        }
    
    def get_max(self):
        if not self.sorted:
            self.width.sort()
            self.height.sort()
            self.sorted = True
        return {
            'width': max(self.width) if self.width else None,
            'height': max(self.height) if self.height else None
        }
        
