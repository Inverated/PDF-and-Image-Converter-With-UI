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
        
        self.widget_stack = QVBoxLayout()
        self.preview_item_list = [PreviewItem(page_no=i+1, document_page_range=[i+1, i+1], curr_size=self.image_size, image='test/download' + str(i + 1) + '.jpg') for i in range(6)]
        for i in range(6):
            self.preview_item_list.append(PreviewItem(page_no=i+1, document_page_range=[i+1, i+1], curr_size=self.image_size, image='test/download' + str(i + 1) + '.jpg'))
        
        for each in self.preview_item_list:
            self.widget_stack.addWidget(each)
            
        container.setLayout(self.widget_stack)
        scroll_area.setWidget(container)        
        items.addWidget(scroll_area)


        option_bar = QHBoxLayout()
        
        compact_checkbox = QCheckBox()
        compact_checkbox.setText('Compact View')
        compact_checkbox.stateChanged.connect(self.set_compact_view)
        
        size_slider = SizeSliderLayout(image_size=self.image_size)
        
        size_slider.connect(self.update_size)
        for i in range(self.widget_stack.count()):
            preview_item_wid:PreviewItem = self.widget_stack.itemAt(i).widget()
            size_slider.connect(preview_item_wid.update_image_size)
            preview_item_wid.removeRequested.connect(self.remove_page)
        
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
        for i in range(self.widget_stack.count()):
            temp:PreviewItem = self.widget_stack.itemAt(i).widget()
            temp.update_page_no(i + 1)
            
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
                    print(start, curr_item)
                    start = start.compact(curr_item)
                else:
                    new_stack.append(start)
                    start = curr_item
            if start != new_stack[-1]:
                new_stack.append(start)
                
            self.preview_item_list = new_stack
            
            self.clear_widget_stack(new_stack)
            for each in new_stack:
                self.widget_stack.addWidget(each)
        
        elif compact == 0:
            #store loaded data in list of list for pdf pages? and retrieve to uncompact 
            return
                
    def clear_widget_stack(self, new_stack):
        while self.widget_stack.count():
            item = self.widget_stack.takeAt(0)
            widget = item.widget()
            if widget is not None and widget not in new_stack:
                widget.deleteLater() 