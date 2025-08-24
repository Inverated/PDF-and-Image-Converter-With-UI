from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStyle, QPushButton
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import QSize

class PreviewItem(QWidget):
    def __init__(self, image = None, page_no = None):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        self.setPalette(palette)
        
        layout = QHBoxLayout()
        
        page_label = QLabel("Pg. " + str(page_no))
        
        image = QLabel()
        pixmap = QPixmap('test/download.jpg')
        image.setPixmap(pixmap)
        image.setFixedSize(pixmap.size())
        
        button = QPushButton()
        pixmap_icon = QStyle.StandardPixmap.SP_DialogDiscardButton
        icon = self.style().standardIcon(pixmap_icon)

        button.setIconSize(QSize(16, 16))
        button.setIcon(icon)

        layout.addWidget(page_label)
        layout.addStretch()
        layout.addWidget(image)
        layout.addStretch()
        layout.addWidget(button)
        
        self.setLayout(layout)
        
        