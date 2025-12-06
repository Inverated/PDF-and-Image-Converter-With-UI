import sys

from PySide6.QtWidgets import QApplication
from palettes import create_dark_palette, create_light_palette
from ui.app import MainWindow
#made by kqf

def main():
    app = QApplication(sys.argv)
 
    window = MainWindow()
    app.setPalette(create_dark_palette())
    window.darkMode.connect(lambda isDark: app.setPalette(create_light_palette() if not isDark else create_dark_palette()))

    window.resize(809, 500)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
