import hashlib
import os
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MyTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Crear el widget de edición de texto
        self.text_editor = QTextEdit()
        self.text_editor.setReadOnly(True)

        # Crear la etiqueta para mostrar el archivo seleccionado
        self.selected_file_label = QLabel("Archivo seleccionado:")

        # Crear el botón para seleccionar un archivo
        self.select_file_button = QPushButton("Seleccionar archivo")
        self.select_file_button.clicked.connect(self.select_file)

        # Configurar el diseño del tab
        layout = QVBoxLayout()
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.selected_file_label)
        layout.addWidget(self.text_editor)
        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Seleccionar archivo", "", "Archivos (*.*)"
        )

        if file_path:
            self.selected_file_label.setText(f"Archivo seleccionado: {file_path}")

            # Calcular el hash
            hash_value = self.calculate_hash(file_path)

            # Obtener la fecha de creación
            creation_date = self.get_creation_date(file_path)

            # Obtener el tamaño del archivo
            file_size = self.get_file_size(file_path)

            # Mostrar los detalles en el widget de edición de texto
            file_details = f"Nombre: {os.path.basename(file_path)}\n"
            file_details += f"Código hash: {hash_value}\n"
            file_details += f"Fecha de creación: {creation_date}\n"
            file_details += f"Tamaño: {file_size}\n"
            self.text_editor.setPlainText(file_details)

    def calculate_hash(self, file_path):
        h = hashlib.md5()
        with open(file_path, "rb") as file:
            block = file.read(4098)
            while block:
                h.update(block)
                block = file.read(4098)

        return h.hexdigest()

    def get_creation_date(self, file_path):
        timestamp = os.path.getctime(file_path)
        creation_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        return creation_date

    def get_file_size(self, file_path):
        size = os.path.getsize(file_path)
        size_str = self.format_size(size)
        return size_str

    def format_size(self, size):
        # Convertir el tamaño del archivo a un formato legible
        units = ["B", "KB", "MB", "GB", "TB"]
        index = 0
        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1
        size_str = f"{size:.2f} {units[index]}"
        return size_str
