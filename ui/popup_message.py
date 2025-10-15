from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QProgressBar

class Popup(QDialog):
    def __init__(self, parent = None, title = "Hi", message = "Message"):
        super().__init__(parent)
        
        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.reject)


        self.layoutbox = QVBoxLayout()
        message = QLabel(message)
        self.layoutbox.addWidget(message)
        
        self.progress = QProgressBar()
        self.progress.hide()
        self.layoutbox.addWidget(self.progress)
        
        self.layoutbox.addWidget(self.buttonBox)
        
        self.setLayout(self.layoutbox)
    
    def setBarRange(self, max:int):
        self.progress.setRange(0, max)
        self.progress.setValue(0)
    
    def setBarVal(self, val:int):
        self.progress.setValue(val)
        
    def finishProgress(self):
        self.progress.setValue(self.progress.maximum())
        self.close()
        self.deleteLater()
    
    def showProgress(self):
        self.progress.show()