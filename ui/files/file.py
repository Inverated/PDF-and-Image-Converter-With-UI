from os.path import splitext

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QImage, QDrag, QPainter
from PySide6.QtCore import QSize, Qt, QMimeData, Signal
from PySide6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions

from ui.display.preview_item import PreviewItem


class File(QWidget):
    removeRequested = Signal(QWidget)
    def __init__(self, path_name):
        super().__init__()
        self.drag_width_px = 200
        self.initial_page_size = 100
        
        self.setObjectName("fileContainer")
        self.setStyleSheet("""
            #fileContainer { border: 2px solid black; }
        """)
        
        with open(path_name, 'rb') as f:
            self.data = f.read()
        
        self.path_name = path_name
        basename, self.extension = splitext(path_name)
        self.document_name = basename.split('/')[-1]
        
        if self.extension == '.pdf':
            self.image_list: list[PreviewItem] = self.__convert_pdf_to_list()        
        else:
            #assume everything else is image?
            self.image_list: list[PreviewItem] = self.__convert_image_to_list()
        
        self.page_count = len(self.image_list)
        #error catch if cannot read
        
        
        # Render simple display
        layout = QHBoxLayout()
        
        label = QLabel(self.file_name())
        
        remove_button = QPushButton()
        trash_pixmap = QStyle.StandardPixmap.SP_DialogDiscardButton
        trash_icon = self.style().standardIcon(trash_pixmap)
        remove_button.setIconSize(QSize(16, 16))
        remove_button.setIcon(trash_icon)
        
        remove_button.clicked.connect(self.__deleteFile)
        
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(remove_button)
        self.setLayout(layout)
        
    def file_name(self):
        return "{}{}\t{} page(s)".format(self.document_name, self.extension, self.page_count)
        
    
    def __convert_image_to_list(self) -> list[PreviewItem]:
        page_range = [1,1]
        image = QImage(self.path_name)
        return [PreviewItem(page_no=1, document_name=self.document_name,
                            document_page_range=page_range, curr_size=self.initial_page_size,
                            image=image)]
         
    def __convert_pdf_to_list(self) -> list[PreviewItem]:
        doc = QPdfDocument()
        doc.load(self.path_name)
        image_list: list[PreviewItem] = []
        
        for page_no in range(doc.pageCount()):
            curr_page = page_no + 1
            page_range = [curr_page, curr_page]
            page_size = doc.pagePointSize(page_no)
            
            width, height = int(page_size.width()), int(page_size.height())

            options = QPdfDocumentRenderOptions()
            options.antialiasing = True
            options.textAntialiasing = True

            rendered_page = doc.render(page_no, QSize(width, height), options)

            # create a white background image
            image = QImage(width, height, QImage.Format_RGB32)
            image.fill(Qt.white)

            # Paint the rendered page on top of the white background
            painter = QPainter(image)
            painter.drawImage(0, 0, rendered_page)
            painter.end()

                    
            #pixmap:fitz.Pixmap = doc.load_page(page_no).get_pixmap()
            #qimg = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            
            image_list.append(PreviewItem(page_no=curr_page, document_name=self.document_name, 
                                          document_page_range=page_range, curr_size=self.initial_page_size,
                                          image=image))
        return image_list
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.file_name())
            drag.setMimeData(mime)
            #Preview drag
            image = self.image_list[0].image_label
            width = image.width()
            height = image.height()
            drag.setPixmap(image.pixmap().scaled(self.drag_width_px, height/width * self.drag_width_px, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            drag.exec(Qt.DropAction.MoveAction)

    def __deleteFile(self):
        self.removeRequested.emit(self)
        