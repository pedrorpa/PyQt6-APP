import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox


def create_new_file():
    app = QApplication.instance()
    file_dialog = QFileDialog()

    file_dialog.setDefaultSuffix("md")
    file_dialog.setNameFilters(["Markdown files (*.md)", "All files (*.*)"])

    file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Crear .md")

    file_dialog.setWindowTitle("Crear nuevo Markdown")
    # Establecer la carpeta predeterminada
    default_folder = "./files/"
    file_dialog.setDirectory(default_folder)

    if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
        selected_file = file_dialog.selectedFiles()[0]
        # Realiza las operaciones necesarias para crear un nuevo archivo Markdown
        with open(selected_file, "w") as file:
            file.write("# New Markdown File")


def open_file():
    app = QApplication.instance()
    file_dialog = QFileDialog()
    file_dialog.setDefaultSuffix("md")
    file_dialog.setNameFilters(["Markdown files (*.md)", "All files (*.*)"])
    file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Abrir .md")
    file_dialog.setWindowTitle("Abrir Markdown")
    default_folder = "./files/"
    file_dialog.setDirectory(default_folder)

    if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
        selected_file = file_dialog.selectedFiles()[0]
        # Aquí puedes realizar las operaciones necesarias para abrir el archivo Markdown seleccionado
        with open(selected_file, "r") as file:
            content = file.read()
            return content


def save_file(content):
    file_dialog = QFileDialog()
    file_dialog.setDefaultSuffix("md")
    file_dialog.setNameFilters(["Markdown files (*.md)", "All files (*.*)"])
    file_dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Guardar")
    file_dialog.setWindowTitle("Guardar Markdown")
    default_folder = "./files/"
    file_dialog.setDirectory(default_folder)

    if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
        selected_file = file_dialog.selectedFiles()[0]
        with open(selected_file, "w") as file:
            file.write(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example usage:
    create_new_file()
    content = open_file()
    if content is not None:
        print(f"File content:\n{content}")
        save_file(content)

    sys.exit(app.exec())
