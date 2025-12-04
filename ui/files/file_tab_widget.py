from os import path as path_of
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QStyle, QFileDialog, QSizePolicy, QFrame, QLabel, QCheckBox, QRadioButton
from PySide6.QtCore import QSize, Signal

from ui.display.preview_content.scroll_area import ScrollArea
from ui.files.file import File

class SideList(QWidget):
    downloadFile = Signal()
    normaliseRequest = Signal(int)
    normaliseChoice = Signal(bool)
    
    def __init__(self):
        super().__init__()     
        self.prev_open_dir = None    #re open open file from same dir
        self.setMinimumWidth(250)   #cannot shrink below
        self.setAcceptDrops(True)
        self.previewStatus = True
        
        layout = QVBoxLayout()

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
        
        selection_area = ScrollArea()
        selection_area.setWidgetResizable(True)
        #selection_area.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        # file stack to contain file widget
        self.file_stack = QVBoxLayout()
        #self.__openTestFiles()
        
        container.setLayout(self.file_stack)
        selection_area.setWidget(container)
        
        #option row
        option_row = QHBoxLayout()
        self.normWidth = QCheckBox()
        self.normWidth.setText("Normalise Width")
        self.normWidth.stateChanged.connect(self.normaliseWidth)
        self.normHeight = QCheckBox()
        self.normHeight.setText("Normalise Height")
        self.normHeight.stateChanged.connect(self.normaliseHeight)
        
        option_row.addStretch()
        option_row.addWidget(self.normWidth)
        option_row.addWidget(self.normHeight)
        
        #option row 2
        option_row2 = QHBoxLayout()
        
        self.isMax = QRadioButton("Max")
        self.isMax.setText("Max")
        self.isMax.toggled.connect(self.normaliseTo)
        
        self.isMin = QRadioButton("Min")
        self.isMin.setText("Min")
        self.isMin.toggled.connect(self.normaliseTo)
        self.isMin.setChecked(True)

        
        option_row2.addStretch()
        option_row2.addWidget(self.isMin)
        option_row2.addWidget(self.isMax)
        
        # Bottom row
        button_row = QHBoxLayout()
        self.status = QLabel()
        self.status.setObjectName("status_label")
        save_button = QPushButton('Save as')
        save_button.clicked.connect(self.__click_save)
        button_row.addWidget(self.status)
        button_row.addStretch()
        button_row.addWidget(save_button)     
        
        layout.addLayout(edit_row)
        layout.addWidget(selection_area, 2)
        layout.addLayout(option_row)
        layout.addLayout(option_row2)
        layout.addLayout(button_row)
        
        self.setLayout(layout)
       
    def setPreviewStatus(self, preview:bool):
        self.previewStatus = preview
        for i in range(0, self.file_stack.count(), 2):
            file:File = self.file_stack.itemAt(i).widget()
            file.setRender(preview)
        
    def set_status_message(self, message, color):
        self.status.setText(message)
        self.status.setStyleSheet("color: {};".format(color))
        
    def add_files(self):
        dialog = QFileDialog()
        selected = dialog.getOpenFileNames(None, "Select 1 or more files to open", dir=self.prev_open_dir, filter="Images/Pdf (*.pdf *.png *.jpg)")
        if len(selected[0]) == 0:
            return
        
        self.prev_open_dir = path_of.dirname(selected[0][0])

        for path in selected[0]:
            self.__addToStack(File(path, self.previewStatus))
        
    def dragEnterEvent(self, event):
        event.accept()
        #do nothing, just hides error cursor
    
    def normaliseTo(self):
        if self.isMin.isChecked():
            self.normaliseChoice.emit(True)
        elif self.isMax.isChecked():
            self.normaliseChoice.emit(False)
        
    def normaliseWidth(self, state):
        if state == 2:
            if self.normHeight.isChecked():
                self.normHeight.blockSignals(True)
                self.normHeight.setChecked(False)
                self.normHeight.blockSignals(False)
            self.normaliseRequest.emit(1)
            
        elif state == 0:
            self.normaliseRequest.emit(0)
        return
    
    def normaliseHeight(self, state):
        if state == 2:
            if self.normWidth.isChecked():
                self.normWidth.blockSignals(True)
                self.normWidth.setChecked(False)
                self.normWidth.blockSignals(False)
            self.normaliseRequest.emit(2)
        elif state == 0:
            self.normaliseRequest.emit(0)
        return
    
    #open from test dir
    '''def __openTestFiles(self):
        files = []
        contents = os.listdir('test')
        for each in contents:
            ext = each[-3:]
            if ext == 'jpg' or ext == 'pdf':
                files.append(File('test/' + each, self.previewStatus))
                
        for item in files:
            self.__addToStack(item)'''
            
            
    def __addToStack(self, item:File):
        self.file_stack.addWidget(item)
        
        #Adding visual seperation line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.file_stack.addWidget(line)
        
        item.removeRequested.connect(self.__removeFile)
        
    def __removeFile(self, file:File):
        index = self.file_stack.indexOf(file)
        file = self.file_stack.itemAt(index).widget()
        line = self.file_stack.itemAt(index + 1).widget()
        
        file.deleteLater()
        line.deleteLater()
        
    def __click_save(self):
        self.downloadFile.emit()
        