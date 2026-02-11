import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt # Importación necesaria para el escalado
from interfaz import VentanaPrincipal

# Optimización para pantallas de alta resolución
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

app = QApplication(sys.argv)
ventana = VentanaPrincipal()
ventana.show()
sys.exit(app.exec())