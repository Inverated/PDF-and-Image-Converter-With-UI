from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

def create_light_palette():
    palette = QPalette()

    # Window background darker gray
    palette.setColor(QPalette.Window, QColor(200, 200, 200))  # slightly darker than bright white
    palette.setColor(QPalette.WindowText, Qt.black)

    # Base widgets (input fields, table cells) slightly colored
    palette.setColor(QPalette.Base, QColor(245, 245, 255))  # light bluish background
    palette.setColor(QPalette.AlternateBase, QColor(225, 235, 250))
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))  # soft tooltip background
    palette.setColor(QPalette.ToolTipText, Qt.black)

    # Buttons
    palette.setColor(QPalette.Button, QColor(210, 220, 230))  # slightly colored buttons
    palette.setColor(QPalette.ButtonText, Qt.black)

    # Highlight / selection
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))  # blue highlight
    palette.setColor(QPalette.HighlightedText, Qt.white)

    return palette

def create_dark_palette():
    palette = QPalette()

    # Window background
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)

    # Base widgets (text input, etc.)
    palette.setColor(QPalette.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)

    # Buttons
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)

    # Highlight / selection
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette