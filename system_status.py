import psutil
from PyQt6.QtWidgets import QLabel


class SystemStatus:
    def __init__(self, parent):
        self.parent = parent
        self.label = QLabel()
        parent.statusBar().addWidget(self.label)

    def update_status(self):
        # Obtener la información del sistema
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("/").percent

        # Actualizar la etiqueta de estado en la ventana principal
        status_text = (
            f"CPU: {cpu_percent}% | Memoria: {memory_percent}% | Disco: {disk_percent}%"
        )
        self.label.setText(status_text)
