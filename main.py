import sys

from markdown_editor import MarkdownEditorApp
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("./css/styles.css", "r") as file:
        style_sheet = file.read()
        # Aplicar estilo de archivo CSS a la aplicación
        app.setStyleSheet(style_sheet)

    window = MarkdownEditorApp()
    window.show()

    sys.exit(app.exec())
