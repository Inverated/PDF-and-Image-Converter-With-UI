from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from ui.file import File

class SideList(QWidget):
    def __init__(self):
        super().__init__()        
        layout = QVBoxLayout()
        
        selection_area = QVBoxLayout()
        self.file_list = File('test/download1.jpg')
        
        
        selection_area.addWidget(self.file_list)
        
        button_row = QHBoxLayout()
        save_button = QPushButton('Save as')
        button_row.addStretch()
        button_row.addWidget(save_button)
        
        
        layout.addLayout(selection_area)
        layout.addStretch()
        layout.addLayout(button_row)
        
        self.setLayout(layout)
        
        
        
        
        
