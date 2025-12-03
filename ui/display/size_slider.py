from PySide6.QtWidgets import QHBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt

class SizeSliderLayout(QHBoxLayout):
    def __init__(self, image_size:int=100):
        super().__init__()
        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(300)
        self.slider.setValue(image_size)
        self.slider.setSingleStep(10)
        self.slider.setFixedWidth(250)
        
        self.label = QLabel(str(image_size) + '%')
        self.slider.valueChanged.connect(self.update_label)
        self.addWidget(self.label)
        self.addWidget(self.slider)
        
    def update_label(self, value):
        step = self.slider.singleStep()
        if value % step != 0:
            self.slider.setValue(round(value/step) * step)
            return

        self.label.setText(str(value) + '%')
        
    def connectValueChanged(self, method):
        self.slider.valueChanged.connect(method)        
    
class Slider(QSlider):
    def __init__(self, orientation):
        super().__init__(orientation)
    
    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        step = self.singleStep()
        snapped = round(self.value() / step) * step
        self.setValue(snapped)
    