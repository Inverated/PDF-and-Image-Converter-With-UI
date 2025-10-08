import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QStyle, QFileDialog
from PySide6.QtCore import QSize

from ui.files.file import File


class SideList(QWidget):
    def __init__(self):
        super().__init__()     
        self.prev_open_dir = "" 
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
        
        selection_area = QScrollArea()
        container = QWidget()
        
        # file stack to contain file widget
        self.file_stack = QVBoxLayout()
        self.__openTestFiles()
        
        container.setLayout(self.file_stack)
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
        dialog = QFileDialog()
        selected = dialog.getOpenFileNames(None, "Select 1 or more files to open", dir=self.prev_open_dir, filter="Images/Pdf (*.pdf *.png *.jpg)")
        self.prev_open_dir = os.path.dirname(selected[0][0])
        #can make this async and add loading bar to File widget?
        for path in selected[0]:
            self.file_stack.addWidget(File(path))
        
    def dragEnterEvent(self, event):
        event.accept()
        #do nothing, just hides error cursor

    #open from test dir
    def __openTestFiles(self):
        files = []
        contents = os.listdir('test')
        for each in contents:
            ext = each[-3:]
            if ext == 'jpg' or ext == 'pdf':
                files.append(File('test/' + each))
                
        for each in files:
            self.file_stack.addWidget(each)