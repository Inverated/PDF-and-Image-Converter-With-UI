from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import Qt

from ui.display.size_slider import SizeSliderLayout

class ScrollArea(QScrollArea):
    linked_slider: SizeSliderLayout = None
    
    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()  # wheel vertical delta
            if self.linked_slider:
                if delta > 0:
                    self.linked_slider.step_up()
                else:
                    self.linked_slider.step_down()
        elif event.modifiers() & Qt.ShiftModifier:
            delta = event.angleDelta().y()  # wheel vertical delta
            scroll_bar = self.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - delta)
        else:
            super().wheelEvent(event)
            
    def setLinkedSlider(self, slider: SizeSliderLayout):
        self.linked_slider = slider