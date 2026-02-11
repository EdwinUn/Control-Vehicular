from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QStackedWidget, QLabel, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView  # <--- Nuevos
)
from PySide6.QtCore import Qt
import vehiculos

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Control Vehicular")
        self.setGeometry(200, 50, 1000, 650)
        
        self.aplicar_estilos()

        # ================== CONTENEDOR PRINCIPAL ==================
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ================== SIDEBAR ==================
        contenedor_menu = QWidget()
        contenedor_menu.setObjectName("sidebar")
        contenedor_menu.setFixedWidth(200)

        menu_layout = QVBoxLayout(contenedor_menu)
        menu_layout.setContentsMargins(10, 20, 10, 20)
        menu_layout.setSpacing(10)

        self.btn_registrar = QPushButton("Registrar / Editar")
        self.btn_buscar = QPushButton("Buscar Vehículo")
        self.btn_multas = QPushButton("Multas")
        self.btn_lista = QPushButton("Lista Vehículos")

        for b in [self.btn_registrar, self.btn_buscar, self.btn_multas, self.btn_lista]:
            b.setMinimumHeight(40)
            menu_layout.addWidget(b)

        menu_layout.addStretch()

        layout_principal.addWidget(contenedor_menu)

        # ================== ÁREA DINÁMICA ==================
        self.stack = QStackedWidget()
        layout_principal.addWidget(self.stack)
        
        # ================== CREAR PANTALLAS ==================
        self.pantalla_formulario()  # index 0
        self.pantalla_buscar()      # index 1
        self.pantalla_multas()      # index 2
        self.pantalla_lista()       # index 3

        # ================== CONEXIONES DEL MENÚ ==================
        self.btn_registrar.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_buscar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_multas.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_lista.clicked.connect(lambda: self.stack.setCurrentIndex(3))


    #Estilos de la página
    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QWidget { color: #d4d4d4; font-family: 'Segoe UI', sans-serif; }
            
            /* Menú Lateral */
            #sidebar { 
                background-color: #252526; 
                border-right: 1px solid #333; 
            }
            
            /* Botones del Menú */
            QPushButton {
                background-color: #2d2d2d;
                color: #cccccc;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3e3e42;
                border-color: #007acc;
                color: white;
            }
            QPushButton:pressed {
                background-color: #007acc;
            }

            /* Inputs */
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 6px;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
            }

            /* Tabla */
            QTableWidget {
                background-color: #252526;
                gridline-color: #333333;
                border: 1px solid #333;
                selection-background-color: #264f78;
                color: white;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #cccccc;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)
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
        self.input_placa_editar.setPlaceholderText("El número de placas sin espacios, guiones o caracteres especiales")

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
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("BÚSQUEDA DE VEHÍCULO")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        self.buscar_placa = QLineEdit()
        self.buscar_placa.setPlaceholderText("El número de placas sin espacios ni símbolos")

        btn = QPushButton("Buscar")
        btn.clicked.connect(self.buscar)

        layout.addWidget(self.buscar_placa)
        layout.addWidget(btn)

        # ===== CONTENEDOR CON SCROLL =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.contenido_busqueda = QWidget()
        self.layout_info = QVBoxLayout(self.contenido_busqueda)

        # ===== DATOS GENERALES (FICHA) =====
        self.labels_info = {}
        campos = ["placa", "marca", "modelo", "anio", "color", "tipo", "propietario", "telefono"]

        for campo in campos:
            lbl = QLabel(f"{campo.capitalize()}: ")
            lbl.setStyleSheet("font-size: 14px; padding:4px;")
            self.labels_info[campo] = lbl
            self.layout_info.addWidget(lbl)

        # ===== MULTAS =====
        titulo_multas = QLabel("MULTAS")
        titulo_multas.setStyleSheet("font-size:16px; font-weight:bold; margin-top:15px;")
        self.layout_info.addWidget(titulo_multas)

        self.tabla_multas = QTableWidget()
        self.tabla_multas.setColumnCount(4)
        self.tabla_multas.setHorizontalHeaderLabels(["Fecha", "Lugar", "Corralón", "# Multas"])
        self.tabla_multas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_multas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_multas.verticalHeader().setVisible(False)

        self.layout_info.addWidget(self.tabla_multas)

        # ===== HISTORIAL =====
        titulo_historial = QLabel("HISTORIAL DE CAMBIOS")
        titulo_historial.setStyleSheet("font-size:16px; font-weight:bold; margin-top:15px;")
        self.layout_info.addWidget(titulo_historial)

        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(2)
        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "Cambio"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_historial.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_historial.verticalHeader().setVisible(False)

        self.layout_info.addWidget(self.tabla_historial)

        scroll.setWidget(self.contenido_busqueda)
        layout.addWidget(scroll)

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
    # 📄 PANTALLA 4 — LISTA (ACTUALIZADA A TABLA)
    # =====================================================
    def pantalla_lista(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("LISTADO GENERAL DE VEHÍCULOS")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        btn = QPushButton("Actualizar Lista")
        btn.clicked.connect(self.listar)
        layout.addWidget(btn)

        # CREACIÓN DE LA TABLA
        self.tabla_vehiculos = QTableWidget()
        self.tabla_vehiculos.setColumnCount(4)
        self.tabla_vehiculos.setHorizontalHeaderLabels(["Placa", "Marca / Modelo", "Propietario", "Estado"])
        
        # Ajuste automático de columnas
        header = self.tabla_vehiculos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.tabla_vehiculos.verticalHeader().setVisible(False)
        
        layout.addWidget(self.tabla_vehiculos)
        self.stack.addWidget(widget)

    def listar(self):
        lista = vehiculos.listar_vehiculos()
        self.tabla_vehiculos.setRowCount(0) # Limpiar tabla
        
        for v in lista:
            row = self.tabla_vehiculos.rowCount()
            self.tabla_vehiculos.insertRow(row)
            
            # Insertar datos en celdas
            self.tabla_vehiculos.setItem(row, 0, QTableWidgetItem(v['placa']))
            self.tabla_vehiculos.setItem(row, 1, QTableWidgetItem(f"{v['marca']} {v['modelo']}"))
            self.tabla_vehiculos.setItem(row, 2, QTableWidgetItem(v['propietario']))
            
            # Celda de estado con color
            item_estado = QTableWidgetItem(v['estado'])
            if v['estado'] == "Activo":
                item_estado.setForeground(Qt.green)
            elif v['estado'] == "Reportado":
                item_estado.setForeground(Qt.red)
                
            self.tabla_vehiculos.setItem(row, 3, item_estado)

    # ================= FUNCIONES LÓGICAS =================

    def registrar(self):
        datos = {k: v.text() for k, v in self.campos_registro.items()}
        datos["placa"] = datos["placa"].upper()

        exito, mensaje = vehiculos.registrar_vehiculo(datos)
        QMessageBox.information(self, "Resultado", mensaje)


    def buscar(self):
        placa = self.buscar_placa.text().strip().upper()
        vehiculo = vehiculos.buscar_por_placa(placa)

        if not vehiculo:
            QMessageBox.warning(self, "Error", "Vehículo no encontrado")
            return

        # ===== DATOS GENERALES =====
        for campo, label in self.labels_info.items():
            valor = vehiculo.get(campo, "—")
            label.setText(f"{campo.capitalize()}: {valor}")

        # ===== MULTAS =====
        multas = vehiculo.get("multas", [])
        self.tabla_multas.setRowCount(0)

        for m in multas:
            row = self.tabla_multas.rowCount()
            self.tabla_multas.insertRow(row)
            self.tabla_multas.setItem(row, 0, QTableWidgetItem(str(m.get("fecha",""))))
            self.tabla_multas.setItem(row, 1, QTableWidgetItem(str(m.get("lugar",""))))
            self.tabla_multas.setItem(row, 2, QTableWidgetItem(str(m.get("corralon",""))))
            self.tabla_multas.setItem(row, 3, QTableWidgetItem(str(m.get("numero_multas",""))))

        # ===== HISTORIAL =====
        historial = vehiculo.get("historial", [])
        self.tabla_historial.setRowCount(0)

        for h in historial:
            row = self.tabla_historial.rowCount()
            self.tabla_historial.insertRow(row)

            if isinstance(h, dict):  # formato nuevo
                self.tabla_historial.setItem(row, 0, QTableWidgetItem(h.get("fecha", "")))
                self.tabla_historial.setItem(row, 1, QTableWidgetItem(h.get("cambio", "")))
            else:  # formato viejo string
                self.tabla_historial.setItem(row, 0, QTableWidgetItem("—"))
                self.tabla_historial.setItem(row, 1, QTableWidgetItem(str(h)))

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