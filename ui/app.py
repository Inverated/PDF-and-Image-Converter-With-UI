from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter, QFileDialog
from PySide6.QtCore import Qt

from backend.file_downloader import Downloader
from ui.display.preview_widget import Preview
from ui.files.file_tab_widget import SideList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.prev_open_dir = None
        
        formats = ('png', 'pnm', 'pgm', 'ppm', 'pbm', 'pam', 'psd', 'ps', 'jpg', 'jpeg')
        ext = " ".join(f"*.{ext}" for ext in formats)
        self.full_extension_filter = "Pdf (*.pdf);; Image ({})".format(ext)
        
        
        self.setWindowTitle("Test")

        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        self.preview_list_widget = Preview()
        self.file_list_widget = SideList()
        
        self.preview_list_widget.downloadItem.connect(self.download_individual)
        self.file_list_widget.downloadFile.connect(self.download_clicked)
        self.file_list_widget.normaliseRequest.connect(self.normaliseImages)
        self.file_list_widget.normaliseChoice.connect(self.setNormaliseChoice)
        
        splitter.addWidget(self.preview_list_widget)
        splitter.addWidget(self.file_list_widget)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        # create custom qsplitterhandle with indicating lines?
        #splitter.setHandleWidth(10)


        #splitter.setSizes([500, 200])
        layout.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def setNormaliseChoice(self, choice):
        self.preview_list_widget.setNormaliseChoice(choice)
        return
    
    def normaliseImages(self, state:0|1|2):
        self.preview_list_widget.previewNormalised(state)
        return
    
    def download_individual(self, item):
        self.download_file(item,  self.full_extension_filter)
        return
    
    def download_clicked(self):
        self.file_list_widget.set_status_message("", "white")
        compacted_list = self.preview_list_widget.get_simplified()
        if len(compacted_list) == 0:
            self.file_list_widget.set_status_message("No files selected", "red")
            return
        
        self.download_file(compacted_list, "Pdf (*.pdf)")
        return

    def download_file(self, lis, filter):
        selected_dir = self.get_download_dir(filter)
        if selected_dir == "":
            #no error message, quit gracefully
            return
        
        downloader = Downloader()
        (status, message) = downloader.downloadFile(lis, selected_dir)
        
        self.file_list_widget.set_status_message(message, "green" if status else "red")

        del downloader
        return
    
    def get_download_dir(self, filter):
        dialog = QFileDialog()
        selected_dir = dialog.getSaveFileName(None, "Save file", self.prev_open_dir if self.prev_open_dir else None, filter=filter)
        dialog.deleteLater()
        return selected_dir[0]
        
