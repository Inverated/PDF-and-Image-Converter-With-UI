from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox, QScrollArea
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from ui.preview_item import PreviewItem

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('red'))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        
        
        items = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        widget_stack = QVBoxLayout()
        for i in range(10):
            widget_stack.addWidget(PreviewItem(page_no= i + 1))
        
        container.setLayout(widget_stack)
        scroll_area.setWidget(container)        
        items.addWidget(scroll_area)


        option_bar = QHBoxLayout()
        
        compact_checkbox = QCheckBox()
        compact_checkbox.setText('Compact View')
        
        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(20)
        size_slider.setMaximum(200)
        size_slider.setSingleStep(5)
        size_slider.setFixedWidth(250)
        
        option_bar.addWidget(compact_checkbox)
        option_bar.addWidget(size_slider)
        
        layout.addLayout(items)
        layout.addLayout(option_bar)
        self.setLayout(layout)
        
