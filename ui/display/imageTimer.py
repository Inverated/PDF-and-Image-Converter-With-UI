from PySide6.QtCore import QTimer, Signal, QObject
from ui.display.size_slider import Slider

class ImageUpdateTimer(QObject):
    valueStopped = Signal()
    
    def __init__(self, interval):
        super().__init__()
        self.delay_timer = QTimer()
        self.delay_timer.setSingleShot(True)
        self.delay_timer.setInterval(interval)

    def set_slider(self, slider: Slider):
        slider.valueChanged.connect(self.on_value_changed)
        self.delay_timer.timeout.connect(self.on_value_stopped)

    def on_value_changed(self):
        self.delay_timer.start()

    def on_value_stopped(self):
        self.valueStopped.emit()
