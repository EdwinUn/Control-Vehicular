from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QStackedWidget, QLabel, QScrollArea
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
        layout_principal = QVBoxLayout(widget)
        layout_principal.setContentsMargins(40, 20, 40, 20)

        # ✅ SOLO UN STACK
        self.stack_form = QStackedWidget()
        layout_principal.addWidget(self.stack_form)

        # =====================================================
        # 🟦 PANTALLA A — MENÚ DE OPCIONES
        # =====================================================
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)

        titulo = QLabel("¿Qué deseas hacer?")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")

        btn_ir_registrar = QPushButton("Registrar Vehículo")
        btn_ir_editar = QPushButton("Editar Vehículo")

        btn_ir_registrar.setMinimumHeight(50)
        btn_ir_editar.setMinimumHeight(50)

        btn_ir_registrar.clicked.connect(lambda: self.stack_form.setCurrentIndex(1))
        btn_ir_editar.clicked.connect(lambda: self.stack_form.setCurrentIndex(2))

        menu_layout.addWidget(titulo)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(btn_ir_registrar)
        menu_layout.addWidget(btn_ir_editar)
        menu_layout.addStretch()

        # 🔥 ESTE FALTABA
        self.stack_form.addWidget(menu_widget)

        # 🟩 REGISTRAR
        self.stack_form.addWidget(self.crear_formulario(modo="registrar"))

        # 🟨 EDITAR
        editar_widget = QWidget()
        editar_layout = QVBoxLayout(editar_widget)

        self.stack_editar = QStackedWidget()
        editar_layout.addWidget(self.stack_editar)

        # PASO 1
        buscar_widget = QWidget()
        buscar_layout = QVBoxLayout(buscar_widget)

        titulo = QLabel("Ingrese la placa a editar")
        titulo.setAlignment(Qt.AlignCenter)

        self.input_placa_editar = QLineEdit()
        self.input_placa_editar.setPlaceholderText("Placa")

        btn_buscar_editar = QPushButton("Buscar Vehículo")
        btn_buscar_editar.clicked.connect(self.cargar_datos_editar)

        btn_volver_menu = QPushButton(" Volver ")
        btn_volver_menu.clicked.connect(lambda: self.stack_form.setCurrentIndex(0))

        buscar_layout.addWidget(titulo)
        buscar_layout.addWidget(self.input_placa_editar)
        buscar_layout.addWidget(btn_buscar_editar)
        buscar_layout.addWidget(btn_volver_menu)
        buscar_layout.addStretch()

        self.stack_editar.addWidget(buscar_widget)

        # PASO 2
        self.form_editar = self.crear_formulario(modo="editar")
        self.stack_editar.addWidget(self.form_editar)

        self.stack_form.addWidget(editar_widget)

        # 👉 AGREGAR ESTA PANTALLA AL STACK PRINCIPAL
        self.stack.addWidget(widget)

    def crear_formulario(self, modo):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        contenedor_form = QWidget()
        form = QFormLayout(contenedor_form)

        campos_local = {}
        labels = ["placa", "marca", "modelo", "anio", "color", "tipo", "propietario", "telefono"]

        for label in labels:
            entrada = QLineEdit()
            campos_local[label] = entrada
            texto_label = "Año" if label == "anio" else label.capitalize()
            form.addRow(texto_label + ":", entrada)


        btn_accion = QPushButton("Guardar")

        if modo == "registrar":
            self.campos_registro = campos_local
            btn_accion.clicked.connect(self.registrar)
        else:
            self.campos_edicion = campos_local
            btn_accion.clicked.connect(self.editar)

        btn_volver = QPushButton(" Volver ")
        btn_volver.clicked.connect(lambda: self.stack_form.setCurrentIndex(0))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(contenedor_form)

        layout.addWidget(scroll)

        layout.addWidget(btn_accion)
        layout.addWidget(btn_volver)
        layout.addSpacing(15)
        layout.addStretch()

        return widget

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
        layout_principal = QVBoxLayout(widget)

        form = QFormLayout()
        layout_principal.addLayout(form)

        self.multa_placa = QLineEdit()
        self.entry_fecha = QLineEdit()
        self.entry_num_multas = QLineEdit()
        self.entry_corralon = QLineEdit()
        self.entry_lugar = QLineEdit()

        form.addRow("Placa", self.multa_placa)
        form.addRow("Fecha", self.entry_fecha)
        form.addRow("# Multas persona", self.entry_num_multas)
        form.addRow("¿Corralón?", self.entry_corralon)
        form.addRow("Lugar", self.entry_lugar)

        btn = QPushButton("Registrar Multa")
        btn.clicked.connect(self.registrar_multa)

        layout_principal.addWidget(btn)
        layout_principal.addStretch()

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
        datos = {k: v.text() for k, v in self.campos_registro.items()}
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
        placa = self.campos_edicion["placa"].text()
        nuevos = {k: v.text() for k, v in self.campos_edicion.items() if k != "placa"}

        exito, mensaje = vehiculos.editar_vehiculo(placa, nuevos)
        QMessageBox.information(self, "Resultado", mensaje)

        self.stack_editar.setCurrentIndex(0)

    def cambiar_estado(self):
        placa = self.campos_edicion["placa"].text()
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
        
    def cargar_datos_editar(self):
        placa = self.input_placa_editar.text().strip().upper()

        vehiculo = vehiculos.buscar_por_placa(placa)
        if not vehiculo:
            QMessageBox.warning(self, "Error", "Vehículo no encontrado")
            return

        # Llenar formulario
        for campo, entrada in self.campos_edicion.items():
            entrada.setText(str(vehiculo.get(campo, "")))

        # La placa no se debe modificar
        self.campos_edicion["placa"].setEnabled(False)

        self.stack_editar.setCurrentIndex(1)

        
    

