from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter, QFileDialog, QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence

from backend.file_downloader import Downloader
from ui.display.preview_content.preview_widget import Preview
from ui.files.file_tab_widget import SideList
from ui.option_bar import OptionBar

class MainWindow(QMainWindow):
    darkMode = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self.prev_open_dir = None
        
        self.formats = ('png', 'pnm', 'pgm', 'ppm', 'pbm', 'pam', 'psd', 'ps', 'jpg', 'jpeg')
        ext = " ".join(f"*.{ext}" for ext in self.formats)
        self.full_extension_filter = f"Pdf (*.pdf);; Image ({ext})"
        self.chosen_image_format = "png"
        
        self.setWindowTitle("PDF and Image Converter")
        self.image_quality = 0  # 0 - High, 1 - Medium, 2 - Low
        
        self.downloader = Downloader(self.image_quality, self.chosen_image_format)
        
        toolba = OptionBar()
        toolba.previewRequested.connect(self.set_preview_state)
        toolba.darkThemeRequested.connect(self.darkMode)
        toolba.imageQualityChanged.connect(lambda quality: setattr(self, 'image_quality', quality))
        self.addToolBar(toolba)
        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(10)
        splitter.show()
        
        self.preview_list_widget = Preview()
        self.file_list_widget = SideList(self.formats)
        
        self.preview_list_widget.downloadItem.connect(self.download_individual)
        self.file_list_widget.downloadFile.connect(self.download_clicked)
        self.file_list_widget.downloadFolder.connect(self.download_folder_clicked)
        self.file_list_widget.normaliseRequest.connect(self.normaliseImages)
        self.file_list_widget.normaliseChoice.connect(self.setNormaliseChoice)
        self.file_list_widget.changeImageFormat.connect(lambda fmt: setattr(self, 'chosen_image_format', fmt))
        
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
        
        self.setContextMenuPolicy(Qt.NoContextMenu)
    
    def set_preview_state(self, enable:bool):
        if not enable:
            self.preview_list_widget.disablePreview()
        self.preview_list_widget.setPreviewStatus(enable)
        self.file_list_widget.setPreviewStatus(enable)
        return
    
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

    def download_file(self, lis, download_filter):
        selected_dir = self.get_download_dir(download_filter)
        if selected_dir == "":
            #no error message, quit gracefully
            return
        
        self.downloader.update(self.image_quality, self.chosen_image_format)
        
        (status, message) = self.downloader.downloadFile(lis, selected_dir, self.preview_list_widget.isNormalised())
        
        self.file_list_widget.set_status_message(message, "green" if status else "red")

    def download_folder_clicked(self):
        self.file_list_widget.set_status_message("", "white")
        directory = self.get_download_folder()
        if directory == "":
            #no error message, quit gracefully
            return

        compacted_list = self.preview_list_widget.get_simplified()
        
        if len(compacted_list) == 0:
            self.file_list_widget.set_status_message("No files selected", "red")
            return
        
        self.downloader.update(self.image_quality, self.chosen_image_format)
        
        (status, message) = self.downloader.downloadFile(compacted_list, directory, self.preview_list_widget.isNormalised())

        self.file_list_widget.set_status_message(message, "green" if status else "red")

    def get_download_dir(self, download_filter):
        dialog = QFileDialog()
        selected_dir = dialog.getSaveFileName(None, "Save file", self.prev_open_dir if self.prev_open_dir else None, filter=download_filter)
        dialog.deleteLater()
        return selected_dir[0]
    
    def get_download_folder(self):
        dialog = QFileDialog()
        selected_dir = dialog.getExistingDirectory(None, "Select folder to save files", self.prev_open_dir if self.prev_open_dir else None)
        dialog.deleteLater()
        return selected_dir
    
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            mimedata = clipboard.mimeData()
            self.file_list_widget.paste_files(mimedata)
            return
        return super().keyPressEvent(event)