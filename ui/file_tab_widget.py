from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea

from ui.file import File

class SideList(QWidget):
    def __init__(self):
        super().__init__()        
        layout = QVBoxLayout()
        
        selection_area = QScrollArea()
        container = QWidget()
        file_stack = QVBoxLayout()
        
        for i in range(6):
            file_stack.addWidget(File('test/download{}.jpg'.format(i + 1)))
        
        container.setLayout(file_stack)
        selection_area.setWidget(container)
         
        button_row = QHBoxLayout()
        save_button = QPushButton('Save as')
        button_row.addStretch()
        button_row.addWidget(save_button)
        
        
        layout.addWidget(selection_area)
        layout.addStretch()
        layout.addLayout(button_row)
        
        self.setLayout(layout)
        
        
        
        
        
