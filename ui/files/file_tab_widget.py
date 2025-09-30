import os
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
        
        testFiles = self.openTestFiles()
        for each in testFiles:
            file_stack.addWidget(each)
        
        
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

    #open from test dir
    def openTestFiles(self) -> list[File]:
        files = []
        contents = os.listdir('test')
        for each in contents:
            ext = each[-3:]
            if ext == 'jpg' or ext == 'pdf':
                files.append(File('test/' + each))
        return files