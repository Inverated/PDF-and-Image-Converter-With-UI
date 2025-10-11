import threading

from os.path import splitext

from time import sleep as i_want_to_sleep

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QImage, QDrag, QPainter, QPixmap
from PySide6.QtCore import QSize, Qt, QMimeData, Signal
from PySide6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions

from ui.display.image import PixMap
from ui.display.preview_image import PreviewImage
from ui.display.preview_item import PreviewItem
from ui.display.preview_pdf import PreviewPdf

class File(QWidget):
    renderComplete = Signal()
    renderProgress = Signal(int)
    
    removeRequested = Signal(QWidget)
    def __init__(self, path_name:str):
        super().__init__()
        self.drag_width_px = 200
        self.initial_page_size = 100
        self.drag_image = None
        
        self.page_count = -1 #initialise
        self.curr_page_no = 0
        self.render_attempt = 0
        
        self.image_list:list[PreviewItem] = []
        self.stop_event_thread = threading.Event()
        
        with open(path_name, 'rb') as f:
            self.data = f.read()
        
        self.path_name = path_name
        basename, self.extension = splitext(path_name)
        self.document_name = basename.split('/')[-1]
        
        # Label tab with name (Create the label before thread as file name will be updated)
        self.label = QLabel()
        self.setFileName()
        
        #Load pdf image seperately
        self.running_thread = threading.Thread(target=self.convert_to_list, daemon=True)
        self.running_thread.start()
        self.renderComplete.connect(self.end_thread)
        self.renderProgress.connect(self.update_progress)
        # Render simple display
        
        layout = QHBoxLayout()
        
        remove_button = QPushButton()
        trash_pixmap = QStyle.StandardPixmap.SP_DialogDiscardButton
        trash_icon = self.style().standardIcon(trash_pixmap)
        remove_button.setIconSize(QSize(16, 16))
        remove_button.setIcon(trash_icon)
        
        remove_button.clicked.connect(self.__deleteFile)
        
        layout.addWidget(self.label)
        
        layout.addStretch()
        layout.addWidget(remove_button)
        self.setLayout(layout)
    
    def end_thread(self):
        self.running_thread.join()
        self.__set_drag_image()
        self.setFileName()
        if self.drag_image == None:
            if self.render_attempt == 3:
                self.label.setText("Unable to render image, please upload again") 
                self.label.setStyleSheet("color: red")  
            else:
                print("Fail " + self.render_attempt)
                self.__re_render()
                self.render_attempt += 1
    
    def __re_render(self):
        self.page_count = -1
        self.curr_page_no = 0
        self.running_thread = threading.Thread(target=self.convert_to_list, daemon=True)
        self.running_thread.start()
        self.renderComplete.connect(self.end_thread)
        self.renderProgress.connect(self.update_progress)
    
    def update_progress(self, curr_page_no):
        self.curr_page_no = curr_page_no
        self.setFileName()
        
    def convert_to_list(self):
        if self.extension == '.pdf':
            self.image_list = self.__convert_pdf_to_list()        
        else:
            self.image_list = self.__convert_image_to_list()
        self.renderComplete.emit()

    def __set_drag_image(self) -> bool:
        if self.image_list == None or len(self.image_list) == 0:
            return
        cover_image = self.image_list[0].image_label
        width = cover_image.width()
        height = cover_image.height()
        scaled_width = self.drag_width_px
        scaled_height = height/width * self.drag_width_px
        scaled_drag = cover_image.pixmap().scaled(self.drag_width_px, height/width * self.drag_width_px, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bg = QPixmap(scaled_width, scaled_height)
        bg.fill(Qt.white)
        
        painter = QPainter(bg)
        painter.drawPixmap(0, 0, scaled_drag)
        painter.end()
        
        self.drag_image = bg
              
    def setFileName(self):      
        if self.page_count == -1 or self.drag_image == None:
            self.label.setText("{}{}\t{}{}".format(self.document_name, self.extension, "Loading...", self.curr_page_no)) 
            self.label.setStyleSheet("color: grey")    
        else:
            self.label.setText("{}{}\t{} page(s)".format(self.document_name, self.extension, self.page_count))
            self.label.setStyleSheet("color: white")    

    
    def __convert_image_to_list(self) -> list[PreviewItem]:
        if self.stop_event_thread.is_set(): # need to add for image if not threading throw error after closing app (still does not work some times)
            return []

        page_range = [1, 1]
        image = QImage(self.path_name)
        i_want_to_sleep(0.01)
        pixmap = PixMap(image, image.width(), image.height())
        
        self.page_count = 1
        self.setFileName()
        return [PreviewImage(page_no=1, document_name=self.document_name, full_path=self.path_name,
                            document_page_range=page_range, curr_size=self.initial_page_size,
                            image=pixmap)]
         
    def __convert_pdf_to_list(self) -> list[PreviewItem]:
        doc = QPdfDocument()
        doc.load(self.path_name)
        image_list: list[PreviewItem] = []
        
        doc_length = doc.pageCount()
        for page_no in range(doc_length):
            if self.stop_event_thread.is_set():
                return []
            curr_page = page_no + 1
            page_range = [curr_page, curr_page]
            page_size = doc.pagePointSize(page_no)
            
            ori_width, ori_height = int(page_size.width()), int(page_size.height())
            
            #rendering at 1.5 times to be slightly clearer (*2 too slow for very large file)
            width, height = ori_width * 1.5, ori_height * 1.5   

            options = QPdfDocumentRenderOptions()
            options.antialiasing = True
            options.textAntialiasing = True

            rendered_page = doc.render(page_no, QSize(width, height), options)

            pixmap = PixMap(rendered_page, ori_width, ori_height)   #scale back to original size with same resolution
            
            image_list.append(PreviewPdf(page_no=curr_page, document_name=self.document_name, full_path=self.path_name,
                                          document_page_range=page_range, curr_size=self.initial_page_size,
                                          image=pixmap))
            try:
                self.renderProgress.emit(page_no)
            except:
                print("App forcefully quit")
                return #app quit
            
        self.page_count = doc_length
        self.setFileName()
        return image_list
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.page_count == -1:
                return
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.label.text())
            drag.setMimeData(mime)
            
            if self.drag_image == None:
                print("Image not rendered properly")
                self.end_thread()
                return
            
            drag.setPixmap(self.drag_image)

            drag.exec(Qt.DropAction.MoveAction)

    def __deleteFile(self):
        self.stop_event_thread.set()
        self.running_thread.join()
        self.removeRequested.emit(self)
        