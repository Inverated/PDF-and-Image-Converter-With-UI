from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QScrollArea

from ui.preview_item import PreviewItem
from ui.size_slider import SizeSliderLayout

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.image_size = 100 #default 100
             
        layout = QVBoxLayout()
            
        items = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        widget_stack = QVBoxLayout()
        self.preview_item_list = [PreviewItem(page_no=i+1, curr_size=self.image_size, image='test/download' + str(i + 1) + '.jpg') for i in range(6)]
        
        for each in self.preview_item_list:
            widget_stack.addWidget(each)
            
        container.setLayout(widget_stack)
        scroll_area.setWidget(container)        
        items.addWidget(scroll_area)


        option_bar = QHBoxLayout()
        
        compact_checkbox = QCheckBox()
        compact_checkbox.setText('Compact View')
        compact_checkbox.stateChanged.connect(self.set_compact_view)
        
        size_slider = SizeSliderLayout(image_size=self.image_size)
        
        size_slider.connect(self.update_size)
        for each in self.preview_item_list:
            size_slider.connect(each.update_image_size)
            each.removeRequested.connect(self.remove_page)
        
        option_bar.addWidget(compact_checkbox)
        option_bar.addStretch()
        option_bar.addLayout(size_slider)
        
        layout.addLayout(items)
        layout.addLayout(option_bar)
        self.setLayout(layout)
        
    def update_size(self, value):
        self.image_size = value
        
    def remove_page(self, page):
        page.setParent(None)
        self.preview_item_list.remove(page)
        for i in range(len(self.preview_item_list)):
            self.preview_item_list[i].update_page_no(i + 1)
            
    def set_compact_view(self, is_compact):
        print(is_compact)