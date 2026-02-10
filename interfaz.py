from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
import vehiculos


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Control Vehicular")
        self.setGeometry(200, 50, 900, 600)

        # ================== CONTENEDOR PRINCIPAL ==================
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout_principal = QHBoxLayout(contenedor)

        # ================== MENÚ LATERAL ==================
        menu = QVBoxLayout()
        layout_principal.addLayout(menu, 1)

        self.btn_registrar = QPushButton("Registrar / Editar")
        self.btn_buscar = QPushButton("Buscar Vehículo")
        self.btn_multas = QPushButton("Multas")
        self.btn_lista = QPushButton("Lista Vehículos")

        for b in [self.btn_registrar, self.btn_buscar, self.btn_multas, self.btn_lista]:
            b.setMinimumHeight(40)
            menu.addWidget(b)

        menu.addStretch()

        # ================== ÁREA DINÁMICA ==================
        self.stack = QStackedWidget()
        layout_principal.addWidget(self.stack, 4)

        # Crear pantallas
        self.pantalla_formulario()
        self.pantalla_buscar()
        self.pantalla_multas()
        self.pantalla_lista()

        # Conexiones del menú
        self.btn_registrar.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_buscar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_multas.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_lista.clicked.connect(lambda: self.stack.setCurrentIndex(3))

# =====================================================
    # 🧾 PANTALLA 1 — REGISTRAR / EDITAR (CORREGIDA)
    # =====================================================
    def pantalla_formulario(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 1. Contenedor del Formulario
        contenedor_form = QWidget()
        form = QFormLayout(contenedor_form)
        
        # Configurar márgenes para que no se vea tan pegado a las orillas
        form.setContentsMargins(10, 10, 10, 10)
        form.setSpacing(10)

        self.campos = {}
        labels = ["placa", "marca", "modelo", "año", "color", "tipo", "propietario", "telefono"]

        for label in labels:
            entrada = QLineEdit()
            self.campos[label] = entrada
            form.addRow(label.capitalize() + ":", entrada)

        # 3. Organización en el Layout Principal de la pantalla
        layout.addWidget(contenedor_form) # Añade el bloque de campos
        layout.addStretch()               # ESTO empuja todo lo anterior hacia arriba

        self.stack.addWidget(widget)
    # =====================================================
    # 🔎 PANTALLA 2 — BUSCAR
    # =====================================================
    def pantalla_buscar(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.buscar_placa = QLineEdit()
        self.buscar_placa.setPlaceholderText("Placa")

        btn = QPushButton("Buscar")
        btn.clicked.connect(self.buscar)

        self.resultado_busqueda = QTextEdit()

        layout.addWidget(self.buscar_placa)
        layout.addWidget(btn)
        layout.addWidget(self.resultado_busqueda)

        self.stack.addWidget(widget)

    # =====================================================
    # 🚨 PANTALLA 3 — MULTAS
    # =====================================================
    def pantalla_multas(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.multa_placa = QLineEdit()
        self.entry_fecha = QLineEdit()
        self.entry_num_multas = QLineEdit()
        self.entry_corralon = QLineEdit()
        self.entry_lugar = QLineEdit()

        layout.addRow("Placa", self.multa_placa)
        layout.addRow("Fecha", self.entry_fecha)
        layout.addRow("# Multas persona", self.entry_num_multas)
        layout.addRow("¿Corralón?", self.entry_corralon)
        layout.addRow("Lugar", self.entry_lugar)

        btn = QPushButton("Registrar Multa")
        btn.clicked.connect(self.registrar_multa)

        layout.addRow(btn)
        self.stack.addWidget(widget)

    # =====================================================
    # 📄 PANTALLA 4 — LISTA
    # =====================================================
    def pantalla_lista(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn = QPushButton("Actualizar Lista")
        btn.clicked.connect(self.listar)

        self.resultado_lista = QTextEdit()

        layout.addWidget(btn)
        layout.addWidget(self.resultado_lista)

        self.stack.addWidget(widget)

    # ================= FUNCIONES LÓGICAS =================

    def registrar(self):
        datos = {k: v.text() for k, v in self.campos.items()}
        datos["placa"] = datos["placa"].upper()

        exito, mensaje = vehiculos.registrar_vehiculo(datos)
        QMessageBox.information(self, "Resultado", mensaje)

    def buscar(self):
        placa = self.buscar_placa.text().strip().upper()
        vehiculo = vehiculos.buscar_por_placa(placa)
        self.resultado_busqueda.clear()

        if not vehiculo:
            QMessageBox.critical(self, "Error", "Vehículo no encontrado")
            return

        info = ""
        for k, v in vehiculo.items():
            if k not in ["historial", "multas"]:
                info += f"{k.capitalize()}: {v}\n"

        info += "\nMultas:\n"
        for m in vehiculo["multas"]:
            info += f"- {m['fecha']} | {m['lugar']} | Corralón: {m['corralon']} | Multas persona: {m['numero_multas']}\n"

        self.resultado_busqueda.setText(info)

    def editar(self):
        placa = self.campos["placa"].text()
        nuevos = {k: v.text() for k, v in self.campos.items() if k != "placa"}
        exito, mensaje = vehiculos.editar_vehiculo(placa, nuevos)
        QMessageBox.information(self, "Resultado", mensaje)

    def cambiar_estado(self):
        placa = self.campos["placa"].text()
        exito, mensaje = vehiculos.cambiar_estado(placa, "Reportado")
        QMessageBox.information(self, "Resultado", mensaje)

    def listar(self):
        lista = vehiculos.listar_vehiculos()
        self.resultado_lista.clear()
        for v in lista:
            self.resultado_lista.append(f"{v['placa']} | {v['marca']} {v['modelo']} | {v['estado']}")

    def registrar_multa(self):
        placa = self.multa_placa.text()
        fecha = self.entry_fecha.text()
        num = self.entry_num_multas.text()
        corralon = self.entry_corralon.text()
        lugar = self.entry_lugar.text()

        exito, mensaje = vehiculos.agregar_multa(placa, fecha, num, corralon, lugar)
        QMessageBox.information(self, "Resultado", mensaje)

