import os

import about_dia
import menu_barra
from my_tab import MyTabWidget
from PyQt6.QtCore import QDateTime, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from system_status import SystemStatus


def convert_markdown_to_html(markdown_text):
    import markdown2

    html_text = markdown2.markdown(markdown_text)
    return html_text


class MarkdownEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proyecto Aplicaciones - Editor de Markdown")
        # DEFINIENDO TAB
        # Crear el QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        # CONTENIDO TAB Markdown Editor
        # Crear el editor de Markdown
        self.markdown_editor = QPlainTextEdit()
        self.markdown_editor.setPlaceholderText("Escribe tu Markdown aquí")

        # Crear el botón de renderizado
        self.render_button = QPushButton("Render Markdown a Html")
        self.render_button.clicked.connect(self.render_markdown)

        # Crear el botón de actualización
        self.refresh_button = QPushButton("Actualizar Lista /files/")
        self.refresh_button.clicked.connect(self.refresh_file_list)

        # Crear el botón de abrir archivo
        self.open_button = QPushButton("Abrir")
        self.open_button.clicked.connect(self.open_selected_file)

        # Crear el botón de eliminar archivo
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_selected_file)

        # Crear el navegador web embebido
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("about:blank"))

        # Crear la lista de archivos
        self.file_list_widget = QListWidget()

        # Obtener la lista de archivos y directorios en la carpeta
        folder_path = "./files/"
        self.update_file_list(folder_path)

        # DISEÑO VENTANA PRINCIPAL MARKDOWN/BOTONES-LISTA FICHEROS/HTML EMBEBIDO

        # Configurar el diseño de la ventana principal
        layout = QHBoxLayout()
        layout.addWidget(self.markdown_editor)

        side_panel = QVBoxLayout()
        side_panel.addWidget(self.render_button)
        side_panel.addWidget(self.refresh_button)
        side_panel.addWidget(self.file_list_widget)
        side_panel.addWidget(self.open_button)
        side_panel.addWidget(self.delete_button)
        layout.addLayout(side_panel)

        # Configurar el navegedor web embebido
        layout.addWidget(self.webview)

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.tab_widget.addTab(main_widget, "MarkDown")
        self.tab_widget.setCurrentIndex(2)
        self.setCentralWidget(self.tab_widget)

        # ---------TAB 2------------
        # SEGUNDO TAB
        custom_tab = MyTabWidget()
        self.tab_widget.addTab(custom_tab, "2º Programa")

        # BARRA SUPERIOR VENTANA

        # Barra de menú
        self.menu_bar = self.menuBar()
        # Menú "File"
        self.file_menu = self.menu_bar.addMenu("Fichero")
        # Acciones del menú "File"
        self.new_action = self.file_menu.addAction("Nuevo")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = self.file_menu.addAction("Abrir")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = self.file_menu.addAction("Guardar como")
        self.save_action.triggered.connect(self.save_file)

        self.close_action = self.file_menu.addAction("Cerrar")
        self.close_action.triggered.connect(self.close)
        # Menú "Help"
        self.help_menu = self.menu_bar.addMenu("Ayuda")
        # Acción "About"
        self.about_action = self.help_menu.addAction("Acerca de")
        self.about_action.triggered.connect(about_dia.show_about_dialog)

        # IMPLEMENTACIÓN ESTADO SISTEMA BARRA INFERIOR VENTANA.

        # Crear el status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        # Crear una etiqueta para mostrar la hora
        self.time_label = QLabel()
        self.status_bar.addWidget(self.time_label)
        # Crear una etiqueta para mostrar el estado del sistema
        self.system_status_label = QLabel()
        self.status_bar.addPermanentWidget(self.system_status_label)
        # Configurar un temporizador para actualizar la hora cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        # Crear una instancia del objeto SystemStatus
        self.system_status = SystemStatus(self)

        # Decido implementarlo en la funcion que actualiza la hora de la ventana para tener el estado actualizado tambien.
        # Obtener el estado del sistema
        # system_status = self.system_status.update_status()
        # Actualizar la etiqueta del estado del sistema
        # self.system_status_label.setText(f"Estado del sistema: {system_status}")

    def update_time(self):
        # Obtener la hora actual
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.system_status.update_status()
        # self.system_status_label.setText(f"Estado del sistema: {system_status}")
        # Actualizar la etiqueta de la hora
        self.time_label.setText(f"Hora: {current_time}")

    def render_markdown(self):
        markdown_text = self.markdown_editor.toPlainText()
        html_text = convert_markdown_to_html(markdown_text)
        self.webview.setHtml(html_text)

    def new_file(self):
        menu_barra.create_new_file()
        self.refresh_file_list()

    def open_file(self):
        content = menu_barra.open_file()
        if content is not None:
            self.markdown_editor.setPlainText(content)

    def save_file(self):
        content = self.markdown_editor.toPlainText()
        menu_barra.save_file(content)
        self.refresh_file_list()

    def update_file_list(self, folder_path):
        self.file_list_widget.clear()
        for file_name in os.listdir(folder_path):
            self.file_list_widget.addItem(file_name)

    def refresh_file_list(self):
        folder_path = "./files/"
        self.update_file_list(folder_path)

    def open_selected_file(self):
        selected_item = self.file_list_widget.currentItem()
        if selected_item is not None:
            file_name = selected_item.text()
            file_path = os.path.join("./files/", file_name)
            with open(file_path, "r") as file:
                content = file.read()
                self.markdown_editor.setPlainText(content)

    def delete_selected_file(self):
        selected_item = self.file_list_widget.currentItem()
        if selected_item is not None:
            file_name = selected_item.text()
            file_path = os.path.join("./files/", file_name)
            os.remove(file_path)
            self.refresh_file_list()
