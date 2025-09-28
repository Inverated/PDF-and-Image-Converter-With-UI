from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QStyle
from PySide6.QtCore import QSize

from ui.files.file import File


class SideList(QWidget):
    def __init__(self):
        super().__init__()      
        self.setAcceptDrops(True)  
  
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: blue;")
        # Top row
        edit_row = QHBoxLayout()
        add_file_button = QPushButton()
        
        folder_icon = QStyle.StandardPixmap.SP_DirOpenIcon
        icon = self.style().standardIcon(folder_icon)
        
        add_file_button.setIconSize(QSize(16, 16))
        add_file_button.setIcon(icon)
        add_file_button.clicked.connect(self.add_files)
        
        edit_row.addStretch()
        edit_row.addWidget(add_file_button)
        
        
        # File list
        selection_area = QScrollArea()
        container = QWidget()
        file_stack = QVBoxLayout()
        for i in range(6):
            file_stack.addWidget(File('test/download{}.jpg'.format(i + 1)))
        
        container.setLayout(file_stack)
        selection_area.setWidget(container)
        
        
        # Bottom row
        button_row = QHBoxLayout()
        save_button = QPushButton('Save as')
        button_row.addStretch()
        button_row.addWidget(save_button)
        
        
        layout.addLayout(edit_row)
        layout.addWidget(selection_area, 2)
        layout.addLayout(button_row)
        
        self.setLayout(layout)
        
    def add_files(self):
        print(123)
        
    def dragEnterEvent(self, event):
        event.accept()
        #do nothing, just hides error cursor

