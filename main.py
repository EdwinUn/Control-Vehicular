"""
Punto de entrada principal de la aplicación de Control Vehicular.

Este script inicializa la instancia de QApplication, configura los atributos
necesarios para el escalado en pantallas de alta densidad (HiDPI) y lanza
la ventana principal de la interfaz gráfica.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt 
from interfaz import VentanaPrincipal

# Configuración de escalado para monitores de alta resolución.
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# Inicialización del objeto de la aplicación con los argumentos del sistema
app = QApplication(sys.argv)

# Creación y visualización de la ventana principal
ventana = VentanaPrincipal()
ventana.show()

# Inicio del bucle de eventos (Event Loop) y cierre ordenado al finalizar
sys.exit(app.exec())