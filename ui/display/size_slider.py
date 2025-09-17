from PySide6.QtWidgets import QHBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt

class SizeSliderLayout(QHBoxLayout):
    def __init__(self, image_size:int=100):
        super().__init__()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(400)
        self.slider.setValue(image_size)
        self.slider.setSingleStep(5)
        self.slider.setFixedWidth(250)
        
        self.label = QLabel(str(image_size) + '%')
        self.slider.valueChanged.connect(self.update_label)
        self.addWidget(self.label)
        self.addWidget(self.slider)
        
    def update_label(self, value):
        self.label.setText(str(value) + '%')
        
    def connect(self, method):
        self.slider.valueChanged.connect(method)

