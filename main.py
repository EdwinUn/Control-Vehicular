
"""
TODO

"""

import sys
from PySide6.QtWidgets import QApplication
from interfaz import VentanaPrincipal

app = QApplication(sys.argv)
ventana = VentanaPrincipal()
ventana.show()
sys.exit(app.exec())
