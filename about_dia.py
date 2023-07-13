from PyQt6.QtWidgets import QMessageBox


def show_about_dialog():
    about_text = """
        <html>
        <head>
            <style>
                h1 {
                    color: Red;
                    font-size: 20px;
                    margin-bottom: 10px;
                }
                p {
                    color: #666;
                    font-size: 14px;
                    margin-bottom: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Acerca de la aplicación</h1>
            <p>Esta es una aplicación de edición de Markdown.</p>
            <p>Desarrollado por: <b>Pedro</b></p>
            <p>Esta aplicación te permite escribir y renderizar texto en formato Markdown. Puedes utilizar las funcionalidades de guardado y apertura de archivos para administrar tus documentos Markdown.</p>
            <p>Disfruta de tu experiencia de edición con esta aplicación y ¡haz que tus documentos se destaquen con Markdown!</p>
        </body>
        </html>
    """
    QMessageBox.about(None, "Acerca de", about_text)
