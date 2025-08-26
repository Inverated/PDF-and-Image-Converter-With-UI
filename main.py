import sys
from PySide6.QtWidgets import QApplication

from ui.app import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setMinimumHeight(700)
    window.setMinimumWidth(600)
    
    window.setMinimumHeight(20)
    window.setMinimumWidth(100)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
