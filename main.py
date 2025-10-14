import sys
import qdarktheme

from PySide6.QtWidgets import QApplication

from ui.app import MainWindow


def main():
    app = QApplication(sys.argv)
 
    window = MainWindow()
    window.darkMode.connect(lambda isDark: app.setPalette(app.style().standardPalette() if not isDark else qdarktheme.load_palette('dark')))
    
    window.resize(809, 500)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
