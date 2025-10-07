from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QScrollArea, QSizePolicy
from PySide6.QtGui import QDropEvent, QDragMoveEvent

from ui.display.preview_item import PreviewItem
from ui.display.size_slider import SizeSliderLayout
from ui.files.file import File
class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.image_size = 100 #default 100
        self.setAcceptDrops(True)  
        layout = QVBoxLayout()
            
        items = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.widget_stack = QVBoxLayout()
            
        container.setLayout(self.widget_stack)
        scroll_area.setWidget(container)        
        items.addWidget(scroll_area)

        option_bar = QHBoxLayout()
        
        compact_checkbox = QCheckBox()
        compact_checkbox.setText('Compact View')
        compact_checkbox.stateChanged.connect(self.set_compact_view)
        
        self.size_slider = SizeSliderLayout(image_size=self.image_size)
        
        self.size_slider.connect(self.update_size)
        self.implementWidgetConnection()
        
        option_bar.addWidget(compact_checkbox)
        option_bar.addStretch()
        option_bar.addLayout(self.size_slider)
        
        layout.addLayout(items)
        layout.addLayout(option_bar)
        self.setLayout(layout)
    
    def implementWidgetConnection(self):
        for i in range(self.widget_stack.count()):
            preview_item_wid:PreviewItem = self.widget_stack.itemAt(i).widget()
            self.size_slider.connect(preview_item_wid.update_image_size)
            preview_item_wid.removeRequested.connect(self.remove_page)
        
    def update_size(self, value):
        self.image_size = value
       
    def reset_page_no(self):
        for i in range(self.widget_stack.count()):
            temp:PreviewItem = self.widget_stack.itemAt(i).widget()
            temp.update_page_no(i + 1)
             
    def remove_page(self, page):
        page.setParent(None)
        self.reset_page_no()
            
    def set_compact_view(self, compact):
        if self.widget_stack.count() == 0:
            return
        
        #0 not checked, 1 partially checked, 2 checked
        if compact == 2:
            start:PreviewItem = self.widget_stack.itemAt(0).widget()
            new_stack:list[PreviewItem] = []
            for i in range(1, self.widget_stack.count()):
                curr_item:PreviewItem = self.widget_stack.itemAt(i).widget()
                if curr_item.document_name == start.document_name and curr_item.document_page_range[0] == start.document_page_range[1] + 1:
                    start = start.compact(curr_item)
                else:
                    new_stack.append(start)
                    start = curr_item
            if start not in new_stack:
                new_stack.append(start)
                        
            self.__clear_widget_stack(new_stack)
            for each in new_stack:
                self.widget_stack.addWidget(each)
                
            self.reset_page_no()
            self.implementWidgetConnection()
        
        elif compact == 0:
            #store loaded data in list of list for pdf pages? and retrieve to uncompact 
            return
                
    def __clear_widget_stack(self, new_stack):
        while self.widget_stack.count():
            item = self.widget_stack.takeAt(0)
            widget = item.widget()
            if widget is not None and widget not in new_stack:
                widget.deleteLater() 
                
    def dragEnterEvent(self, event):
        event.accept()
    
    def __findTargetLocation(self, event:QDropEvent | QDragMoveEvent):
        pos = event.position().toPoint()
        container_pos = self.widget_stack.parentWidget().mapFrom(self, pos)
        
        n = 0
        for n in range(self.widget_stack.count()):
            each:PreviewItem = self.widget_stack.itemAt(n).widget()
            
            if container_pos.y() < each.y() + each.size().height() // 2:
                break
        else:
            #End of stack
            n += 1
        return n
    
    def dropEvent(self, event:QDropEvent):
        type_of = type(event.source())
        if type_of == File:
            self.__addFromFileList(event)
        elif type_of == PreviewItem:
            self.__reorderInternalItems(event)
        
        event.accept()
        self.resetIndicators()
        self.reset_page_no()
    
    def __addFromFileList(self, event:QDropEvent):
        widget:File = event.source()
        n = self.__findTargetLocation(event)

        if self.widget_stack.count() == 0:
            n = 0
            
        for i, item in enumerate(widget.image_list):
            item_copy = item.copyOf()
            item_copy.update_image_size(self.image_size)
            self.widget_stack.insertWidget(n + i, item_copy)
        self.implementWidgetConnection()


    def __reorderInternalItems(self, event:QDropEvent):
        if self.widget_stack.count() <= 1:
            #no use sorting if 1 item
            return
        
        widget:PreviewItem = event.source()        
        self.widget_stack.removeWidget(widget)
        
        n = self.__findTargetLocation(event)
        self.widget_stack.insertWidget(n, widget)
        
    def dragMoveEvent(self, event:QDragMoveEvent):
        if self.widget_stack.count() == 0:
            return 
        
        n = self.__findTargetLocation(event)
        
        if n == self.widget_stack.count():
            widget:PreviewItem = self.widget_stack.itemAt(n - 1).widget()
            widget.set_top_indicator(show=False)
            widget.set_bottom_indicator(show=True)
            return
        
        widget:PreviewItem = self.widget_stack.itemAt(n).widget()
        widget.set_top_indicator(show=True)
        widget.set_bottom_indicator(show=False)
        
        if n == 0:
            if self.widget_stack.count() != 1:
                temp:PreviewItem = self.widget_stack.itemAt(n+1).widget()
                temp.set_top_indicator(show=False)
        elif n == self.widget_stack.count() - 1:
            temp:PreviewItem = self.widget_stack.itemAt(n-1).widget()
            temp.set_top_indicator(show=False)
            temp.set_bottom_indicator(show=False)
        elif n > 0:
            temp:PreviewItem = self.widget_stack.itemAt(n-1).widget()
            temp.set_top_indicator(show=False)
            temp.set_bottom_indicator(show=False)
            
            temp:PreviewItem = self.widget_stack.itemAt(n+1).widget()
            temp.set_top_indicator(show=False)
            temp.set_bottom_indicator(show=False)
        
        event.accept()
    
    def resetIndicators(self):
        for n in range(self.widget_stack.count()):
            widget:PreviewItem = self.widget_stack.itemAt(n).widget()
            widget.set_bottom_indicator(show=False)
            widget.set_top_indicator(show=False)
    
    def dragLeaveEvent(self, event):
        self.resetIndicators()
        event.accept()
            
            