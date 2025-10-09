from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter, QFileDialog
from PySide6.QtCore import Qt

from backend.file_downloader import Downloader
from ui.display.preview_widget import Preview
from ui.files.file_tab_widget import SideList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.prev_open_dir = None
        
        self.setWindowTitle("Test")

        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        self.preview_list_widget = Preview()
        file_list_widget = SideList()
        
        file_list_widget.downloadFile.connect(self.download_clicked)
        
        splitter.addWidget(self.preview_list_widget)
        splitter.addWidget(file_list_widget)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        # create custom qsplitterhandle with indicating lines?
        #splitter.setHandleWidth(10)


        #splitter.setSizes([500, 200])
        layout.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def download_clicked(self):
        dialog = QFileDialog()
        selected_dir = dialog.getSaveFileName(None, "Open dir", self.prev_open_dir if self.prev_open_dir else None)
        downloader = Downloader()
        
        compacted_list = self.preview_list_widget.get_simplified()
        if len(compacted_list) == 0:
            return
        
        downloader.downloadFile(compacted_list, selected_dir)
        del downloader
        return
