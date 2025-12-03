import threading
import time

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QScrollArea, QSizePolicy, QPushButton, QMessageBox
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDropEvent, QDragMoveEvent

from ui.display.image import PixMap
from ui.display.preview_item import PreviewItem
from ui.display.size_slider import SizeSliderLayout

from ui.display.imageTimer import ImageUpdateTimer
from ui.files.file import File
from ui.popup_message import Popup

class Preview(QWidget):
    downloadItem = Signal(list)
    progressRange = Signal(int)
    progressProgress = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.image_size = 100 #default 100
        self.time_counter = 0
        self.max_width = self.max_height  = -1
        self.min_height = self.min_width = 99999 
        self.normalisedState = 0
        self.normalisedWidth = True
        self.previewStatus = True
        self.sizeUpdateTimer = {'start':0, 'end':0}
        self.skipUpdate = False
        
        self.runningThread = None
        self.dialog = None
        
        self.setAcceptDrops(True)  
        layout = QVBoxLayout()
        
        option_bar2 = QHBoxLayout()
        delAll = QPushButton("Delete All")
        option_bar2.addStretch()
        option_bar2.addWidget(delAll)
        delAll.clicked.connect(self.__clearAllWidget)
        
        items = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_bar = self.scroll_area.verticalScrollBar()
        self.scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.widget_stack = QVBoxLayout()
            
        container.setLayout(self.widget_stack)
        self.scroll_area.setWidget(container)        
        items.addWidget(self.scroll_area)

        self.maxHeight = self.scroll_bar.height()
        self.scroll_threshold = [0.3 * self.maxHeight, 0.15 * self.maxHeight, 0.1 * self.maxHeight]
        
        option_bar = QHBoxLayout()
        
        self.compact_checkbox = QCheckBox()
        self.compact_checkbox.setText('Compact View')
        self.compact_checkbox.stateChanged.connect(self.set_compact_view)
        
        self.size_slider = SizeSliderLayout(image_size=self.image_size)
        
        self.timer = ImageUpdateTimer(interval=100)
        self.timer.valueStopped.connect(self.setFinalSizing)
        self.size_slider.connectValueChanged(self.update_size)
        self.implementWidgetConnection()
        
        option_bar.addWidget(self.compact_checkbox)
        option_bar.addStretch()
        option_bar.addLayout(self.size_slider)
        
        layout.addLayout(option_bar2)
        layout.addLayout(items)
        layout.addLayout(option_bar)
        self.setLayout(layout)
    
    def setPreviewStatus(self, status):
        self.previewStatus = status
    
    def disablePreview(self):
        new_list:list[PreviewItem] = []
        del_list:list[PreviewItem] = []
        size = self.widget_stack.count()
        for i in range(size):
            item:PreviewItem = self.widget_stack.itemAt(i).widget()
            if item.image_label.pixmap().isNull():
                new_list.append(item)
            else:
                new_list.append(item.disablePreview())
                del_list.append(item)
                
        for each in new_list:
            each.setParent(None)
            self.widget_stack.addWidget(each)
        for each in del_list:
            each.deleteLater()
        self.implementWidgetConnection()
            
    def __clearAllWidget(self):            
        self.max_width = self.max_height  = -1
        self.min_height = self.min_width = 99999 
        while self.widget_stack.count():
            self.widget_stack.takeAt(0).widget().deleteLater()
        return
    
    def isNormalised(self):
        return self.normalisedState != 0
    
    def setNormaliseChoice(self, choice:bool):
        if self.normalisedWidth != choice:
            self.normalisedWidth = choice
            self.previewNormalised(self.normalisedState) if self.normalisedState != 0 else None
    
    def __normaliseImage(self, preview_item_wid:PreviewItem):
        preview_item_image:PixMap = preview_item_wid.getImage()
        preview_item_image.resetNorm()
        match (self.normalisedState):
            case 1:
                preview_item_image.normaliseWidth(self.min_width if self.normalisedWidth else self.min_height)
            case 2:
                preview_item_image.normaliseHeight(self.min_height if self.normalisedWidth else self.max_height)
        preview_item_wid.update_image_size(self.image_size)
        
    def previewNormalised(self, state:0|1|2): #0 - reset; 1 - width; 2 - height
        self.normalisedState = state
        for i in range(self.widget_stack.count()):
            preview_item_wid:PreviewItem = self.widget_stack.itemAt(i).widget()
            self.__normaliseImage(preview_item_wid)
    
    def implementWidgetConnection(self):
        self.size_slider.connectValueChanged(self.__triggerUpdateSize)
        self.timer.set_slider(self.size_slider.slider)
        for i in range(self.widget_stack.count()):
            preview_item_wid:PreviewItem = self.widget_stack.itemAt(i).widget()            
            preview_item_wid.removeRequested.connect(self.remove_page, Qt.ConnectionType.UniqueConnection)               
            preview_item_wid.downloadRequested.connect(self.download_item, Qt.ConnectionType.UniqueConnection)
            preview_item_wid.update_image_size(self.image_size)
    
    def __triggerUpdateSize(self):
        if self.skipUpdate:
            return
        
        if self.sizeUpdateTimer['start'] == 0:
            self.sizeUpdateTimer['start'] = time.time()
            
        self.updateSize()
        self.sizeUpdateTimer['end'] = time.time()
        
        time_taken = self.sizeUpdateTimer['end'] - self.sizeUpdateTimer['start']
        if time_taken > 0.05:
            self.skipUpdate = True
        self.sizeUpdateTimer['start'] = 0
    
    def setFinalSizing(self):
        self.skipUpdate = False
        self.sizeUpdateTimer['start'] = 0
        self.sizeUpdateTimer['end'] = 0
        self.updateSize()
    
    def updateSize(self):
        for i in range(self.widget_stack.count()):
            preview_item_wid:PreviewItem = self.widget_stack.itemAt(i).widget()            
            preview_item_wid.update_image_size(self.image_size)
            
    def download_item(self, item):
        self.downloadItem.emit(item)
        
    def update_size(self, value):
        value = round(value / 10) * 10
        self.image_size = value
       
    def __reset_page_no(self):
        curr_page_no = 1
        for i in range(self.widget_stack.count()):
            temp:PreviewItem = self.widget_stack.itemAt(i).widget()
            temp.update_page_no(curr_page_no)
            docRange = temp.document_page_range
            curr_page_no += docRange[1] - docRange[0] + 1
            temp.set_bottom_indicator(show=False)
            temp.set_top_indicator(show=False)
             
    def remove_page(self, page:PreviewItem):
        page.setParent(None)
        self.__update_saved_size(page, is_new=False)
        page.deleteLater()
        self.__reset_page_no()
        
    
    def __find_val(self, find_min:bool = True, find_width:bool = True):
        item:PreviewItem = self.widget_stack.itemAt(0).widget()
        val = item.getImage().getWidth() if find_width else item.getImage().getHeight()
        for i in range(1, self.widget_stack.count()):
            item:PreviewItem = self.widget_stack.itemAt(i).widget()
            if find_min:
                val = item.image.getWidth() if find_width and item.image.getWidth() < val else val
                val = item.image.getHeight() if not find_width and item.image.getHeight() < val else val
            else:
                val = item.image.getWidth() if find_width and item.image.getWidth() > val else val
                val = item.image.getHeight() if not find_width and item.image.getHeight() > val else val
        return val       
            
    def __update_saved_size(self, page:PreviewItem, is_new = True): #change to a better data structure later
        new_width = page.image.getWidth()
        new_height = page.image.getHeight()
        if not is_new:
            if self.widget_stack.count() == 0:
                self.max_width = self.max_height  = -1
                self.min_height = self.min_width = 99999 
                return
            if new_width == self.min_width:
                self.min_width = self.__find_val(True, True)
            if new_width == self.max_width:
                self.max_width = self.__find_val(False, True)
            if new_height == self.min_height:
                self.min_height = self.__find_val(True, False)
            if new_height == self.max_height:
                self.max_height = self.__find_val(False, False)
        else:
            if new_width > self.max_width:
                self.max_width = new_width
            if new_width < self.min_width:
                self.min_width = new_width
            if new_height > self.max_height:
                self.max_height = new_height
            if new_height < self.min_height:
                self.min_height = new_height
    
    def start_new_thread(self, method, *args):
        self.dialog = Popup(self)
        
        self.runningThread = threading.Thread(method, args=args, daemon=True)
        self.progressRange.connect(self.dialog.setBarRange, Qt.ConnectionType.UniqueConnection)
        self.progressProgress.connect(self.dialog.setBarVal, Qt.ConnectionType.UniqueConnection)
        
        if not self.dialog.exec_():
            print('cx')
    
    def end_thread(self):
        if not self.dialog == None:
            self.runningThread.join()
            self.dialog.finishProgress()
            
    def set_compact_view(self, compact):
        if self.widget_stack.count() == 0:
            return
        
        #0 not checked, 1 partially checked, 2 checked
        if compact == 2:
            self.__compactList()
        
        elif compact == 0:
            self.__unCompactList()
    
    def __compactList(self):
        start:PreviewItem = self.widget_stack.itemAt(0).widget()
        new_stack:list[PreviewItem] = []
        
        for i in range(0, self.widget_stack.count()):
            curr_item:PreviewItem = self.widget_stack.itemAt(0).widget()
            curr_item.setParent(None)
            if curr_item.document_name == start.document_name and curr_item.document_page_range[0] == start.document_page_range[1] + 1:
                start = start.compact(curr_item)
            else:
                new_stack.append(start)
                start = curr_item
                
        if not start == new_stack[-1]:
            new_stack.append(start)
                    
        #self.__clear_unused_widget_stack(new_stack)
        for each in new_stack:
            self.widget_stack.addWidget(each)
            
        self.__reset_page_no()
        self.implementWidgetConnection()
    
    def __unCompactList(self):
        #store loaded data in list of list for pdf pages? and retrieve to uncompact 
        new_stack:list[PreviewItem] = []
        for _ in range(self.widget_stack.count()):
            item:PreviewItem = self.widget_stack.itemAt(0).widget()
            contains = item.uncompact()
            new_stack.append(item)
            if contains != None:
                new_stack.extend(contains)
            item.setParent(None)
                
        for each in new_stack:
            self.widget_stack.addWidget(each)
            self.__normaliseImage(each)       
        
        self.__reset_page_no()
        self.implementWidgetConnection()
        return
    
    '''def __clear_unused_widget_stack(self, new_stack):
        while self.widget_stack.count():
            item = self.widget_stack.takeAt(0)
            widget = item.widget()
            if widget is not None and widget not in new_stack:
                widget.setParent(None) '''
                
    def dragEnterEvent(self, event):
        event.accept()
    
    def __updateScrollHeight(self):
        self.maxHeight = self.scroll_bar.height()
        self.scroll_threshold = [0.3 * self.maxHeight, 0.15 * self.maxHeight, 0.1 * self.maxHeight]
        
    def __edgeScroll(self, cursorY:int):     
        if cursorY < self.scroll_threshold[0]:
            if cursorY < self.scroll_threshold[2]:
                self.scroll_bar.setValue(self.scroll_bar.value() - 15)
            if cursorY < self.scroll_threshold[1]:
                self.scroll_bar.setValue(self.scroll_bar.value() - 10)
            else:
                self.scroll_bar.setValue(self.scroll_bar.value() - 50)
                
        elif cursorY > self.maxHeight - self.scroll_threshold[0]:
            if cursorY > self.maxHeight - self.scroll_threshold[2]:
                self.scroll_bar.setValue(self.scroll_bar.value() + 15)
            elif cursorY > self.maxHeight - self.scroll_threshold[1]:
                self.scroll_bar.setValue(self.scroll_bar.value() + 10)
            else:
                self.scroll_bar.setValue(self.scroll_bar.value() + 5)
            
    def __findTargetLocation(self, event:QDropEvent | QDragMoveEvent):
        pos = event.position().toPoint()
        container_pos = self.widget_stack.parentWidget().mapFrom(self, pos)
        
        if self.maxHeight != self.scroll_area.height():
            self.__updateScrollHeight()
            
        self.__edgeScroll(pos.y())

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
        widget = event.source()
        if isinstance(widget, File):
            self.__addFromFileList(event)
        elif isinstance(widget, PreviewItem):
            self.__reorderInternalItems(event)
            
        event.accept()
        self.__reset_page_no()
    
    def __addFromFileList(self, event:QDropEvent):
        widget:File = event.source()
        n = self.__findTargetLocation(event)

        if self.widget_stack.count() == 0:
            n = 0

        if self.compact_checkbox.isChecked():
            for item in widget.image_list:
                self.__update_saved_size(item, is_new=True)
            
            if self.previewStatus:
                first:PreviewItem = widget.image_list[0].copyOf()
                first.compact_list([each.copyOf() for each in widget.image_list[1:]])
            else:
                first:PreviewItem = widget.image_list[0].disablePreview()
                first.compact_list([each.disablePreview() for each in widget.image_list[1:]])
            first.update_image_size(self.image_size)
            self.widget_stack.insertWidget(n, first)
            self.__normaliseImage(first)
        else:
            for i, item in enumerate(widget.image_list):
                self.__update_saved_size(item, is_new=True)
                if self.previewStatus:
                    item_copy:PreviewItem = item.copyOf()
                else:
                    item_copy:PreviewItem = item.disablePreview()    
                item_copy.update_image_size(self.image_size)
                self.widget_stack.insertWidget(n + i, item_copy)
                self.__normaliseImage(item)
                
        self.implementWidgetConnection()
        return

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
        
    def get_simplified(self):
        if self.widget_stack.count() == 0:
            # add prompt user 
            return []
        
        #start:PreviewItem = self.widget_stack.itemAt(0).widget().copyOf()
        new_stack:list[PreviewItem] = []
        
        """ for i in range(1, self.widget_stack.count()):
            curr_item:PreviewItem = self.widget_stack.itemAt(i).widget()
            if curr_item.document_name == start.document_name and curr_item.document_page_range[0] == start.document_page_range[1] + 1:
                start = start.compact(curr_item)
            else:
                new_stack.append(start)
                start = curr_item.copyOf()
        if start not in new_stack:
            new_stack.append(start) """
            
        for i in range(0, self.widget_stack.count()):
            new_stack.append(self.widget_stack.itemAt(i).widget())
        
        return new_stack
        