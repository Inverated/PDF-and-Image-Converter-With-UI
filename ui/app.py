from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt

from ui.display.preview_widget import Preview
from ui.files.file_tab_widget import SideList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(Preview())
        splitter.addWidget(SideList())

        # create custom qsplitterhandle with indicating lines?
        splitter.setHandleWidth(10)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background: dark-gray;
            }
        """)

        splitter.setSizes([500, 200])
        layout.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
