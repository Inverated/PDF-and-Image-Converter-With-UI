from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt
from ui.preview_widget import Preview


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(Preview())
        splitter.addWidget(QWidget())
        
        #create custom qsplitterhandle?
        splitter.setHandleWidth(10)

        splitter.setSizes([500, 200])
        layout.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
