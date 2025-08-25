from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox, QScrollArea
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from ui.preview_item import PreviewItem

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.image_size = 100
             
        layout = QVBoxLayout()
        
        
        items = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        widget_stack = QVBoxLayout()
        self.preview_item_list = [PreviewItem(curr_size=self.image_size, page_no=i+1) for i in range(10)]
        
        for each in self.preview_item_list:
            widget_stack.addWidget(each)
            
        container.setLayout(widget_stack)
        scroll_area.setWidget(container)        
        items.addWidget(scroll_area)


        option_bar = QHBoxLayout()
        
        compact_checkbox = QCheckBox()
        compact_checkbox.setText('Compact View')
        
        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(20)
        size_slider.setMaximum(200)
        size_slider.setValue(self.image_size)
        size_slider.setSingleStep(5)
        size_slider.setFixedWidth(250)
        size_slider.valueChanged.connect(self.update_size)
        for each in self.preview_item_list:
            size_slider.valueChanged.connect(each.update_image_size)
            each.removeRequested.connect(self.remove_page)
        
        
        option_bar.addWidget(compact_checkbox)
        option_bar.addWidget(size_slider)
        
        layout.addLayout(items)
        layout.addLayout(option_bar)
        self.setLayout(layout)
        
    def update_size(self, value):
        self.image_size = value
        print(value)
        
    def remove_page(self, page):
        page.setParent(None)
        self.preview_item_list.remove(page)
        for i in range(len(self.preview_item_list)):
            self.preview_item_list[i].update_page_no(i + 1)