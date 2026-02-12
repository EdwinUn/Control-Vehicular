from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QStackedWidget, QLabel, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout
)
from PySide6.QtCore import Qt
from datetime import datetime
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

        self.stack_form.currentChanged.connect(self.reset_scroll_automatico)

    def reset_scroll_automatico(self, index):
        if hasattr(self, "scroll_registro"):
            self.scroll_registro.verticalScrollBar().setValue(0)
        if hasattr(self, "scroll_edicion"):
            self.scroll_edicion.verticalScrollBar().setValue(0)

    #Estilos de la página
    def aplicar_estilos(self):
        self.setStyleSheet("""
            /* ===== FONDO BASE ===== */
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-size: 14px;
            }

            /* ===== SIDEBAR ===== */
            #sidebar {
                background-color: #252526;
                border-right: 1px solid #3c3c3c;
            }

            /* ===== ÁREA PRINCIPAL ===== */
            QStackedWidget, QStackedWidget QWidget {
                background-color: #2d2d30;
            }

            /* ===== INPUTS ESTILO LÍNEA ===== */
            QLineEdit {
                background: transparent;
                border: none;
                border-bottom: 1px solid #555;
                padding: 8px 4px 4px 4px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border-bottom: 2px solid #5c9ded;
            }

            QLineEdit::placeholder {
                color: #888;
            }

            /* ===== BOTONES ===== */
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #444;
                padding: 8px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #4a4a4a;
            }

            /* ===== TABLAS ===== */
            QTableWidget {
                background-color: #2b2b2b;
                gridline-color: #3c3c3c;
                border: 1px solid #3c3c3c;
            }

            QTableWidget::item {
                background-color: #2b2b2b;
            }

            QHeaderView::section {
                background-color: #333333;
                border: 1px solid #3c3c3c;
                padding: 5px;
            }
        """)

    def volver_formulario(self):
            # 1. Limpiar campos de texto
            if hasattr(self, "campos_edicion"):
                for campo in self.campos_edicion.values():
                    campo.clear()
                    campo.setEnabled(True) # Re-habilitar la placa por si estaba bloqueada

            if hasattr(self, "campos_registro"):
                for campo in self.campos_registro.values():
                    campo.clear()

            # 2. Resetear el sub-stack de edición al paso 1 (Pedir placa)
            if hasattr(self, "stack_editar"):
                self.stack_editar.setCurrentIndex(0)
                self.input_placa_editar.clear() # Limpia la placa que escribiste antes

            # 3. Resetear scrolls (Lo que ya tenías)
            if hasattr(self, "scroll_edicion"):
                self.scroll_edicion.verticalScrollBar().setValue(0)
            if hasattr(self, "scroll_registro"):
                self.scroll_registro.verticalScrollBar().setValue(0)

            # 4. Regresar al menú de "¿Qué deseas hacer?"
            self.stack_form.setCurrentIndex(0)


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
        btn_volver_menu.clicked.connect(self.volver_formulario)

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
        contenedor_scroll = QScrollArea()
        contenedor_scroll.setWidgetResizable(True)
        contenedor_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widget = QWidget()
        layout_principal = QVBoxLayout(widget)
        layout_principal.setContentsMargins(80, 30, 80, 30)
        layout_principal.setSpacing(18)

        # 🔥 CLAVE: que todo empiece arriba e izquierda
        layout_principal.setAlignment(Qt.AlignTop | Qt.AlignLeft)

                # ===== ENCABEZADO =====
        titulo = QLabel("Registro de Vehículo" if modo == "registrar" else "Editar Vehículo")
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
        """)
        titulo.setAlignment(Qt.AlignLeft)

        subtitulo = QLabel("Completa la información del vehículo")
        subtitulo.setStyleSheet("font-size: 14px; color: gray;")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)
        layout_principal.addSpacing(15)

        campos_local = {}

        def bloque_input(texto_label):
            cont = QWidget()
            cont_layout = QVBoxLayout(cont)
            cont_layout.setSpacing(6)
            cont_layout.setAlignment(Qt.AlignLeft)

            label = QLabel(texto_label)
            label.setStyleSheet("font-weight: bold; font-size:14px;")

            entrada = QLineEdit()
            entrada.setMinimumHeight(38)
            entrada.setMaximumWidth(500)


            cont_layout.addWidget(label)
            cont_layout.addWidget(entrada)
            return cont, entrada

        campos = [
            ("Placa", "placa"),
            ("Marca", "marca"),
            ("Modelo", "modelo"),
            ("Año", "anio"),
            ("Color", "color"),
            ("Tipo de vehículo", "tipo"),
            ("Propietario", "propietario"),
            ("Teléfono", "telefono")
        ]

        for texto, key in campos:
            bloque, entrada = bloque_input(texto)
            layout_principal.addWidget(bloque, alignment=Qt.AlignLeft)
            campos_local[key] = entrada

        # ===== BOTONES =====
        layout_principal.addSpacing(10)

        btn_accion = QPushButton("Guardar")
        btn_accion.setMinimumHeight(45)
        btn_accion.setMaximumWidth(300)

        if modo == "registrar":
            self.campos_registro = campos_local
            btn_accion.clicked.connect(self.registrar)
        else:
            self.campos_edicion = campos_local
            btn_accion.clicked.connect(self.editar)

        btn_volver = QPushButton("Volver")
        btn_volver.setMaximumWidth(300)
        btn_volver.clicked.connect(self.volver_formulario)

        # 🔥 también alineados a la izquierda
        layout_principal.addWidget(btn_accion, alignment=Qt.AlignLeft)
        layout_principal.addWidget(btn_volver, alignment=Qt.AlignLeft)

        layout_principal.addStretch()

        contenedor_scroll.setWidget(widget)
        
        # guarda referencia para poder manipularlo luego
        if modo == "registrar":
            self.scroll_registro = contenedor_scroll
        else:
            self.scroll_edicion = contenedor_scroll

        return contenedor_scroll


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
        self.layout_info.setSpacing(8)  # 👈 Espacio general entre bloques

        # ===== DATOS GENERALES =====
        self.labels_info = {}
        # La clave sigue siendo "anio" para el backend, 
        # pero el texto del Label será "Año"
        campos = [
            ("placa", "Placa"),
            ("marca", "Marca"),
            ("modelo", "Modelo"),
            ("anio", "Año"),
            ("color", "Color"),
            ("tipo", "Tipo"),
            ("propietario", "Propietario"),
            ("telefono", "Teléfono")
        ]

        for clave_json, texto_visual in campos:
            lbl = QLabel(f"{texto_visual}: ")
            lbl.setStyleSheet("font-size: 14px; padding:4px;")
            self.labels_info[clave_json] = lbl # Guardamos la referencia con la clave del JSON
            self.layout_info.addWidget(lbl)

        # ===== MULTAS =====
        titulo_multas = QLabel("MULTAS")
        titulo_multas.setStyleSheet("font-size:16px; font-weight:bold; margin-top:15px;")
        self.layout_info.addWidget(titulo_multas)

        self.tabla_multas = QTableWidget()
        self.tabla_multas.setColumnCount(4)
        self.tabla_multas.setHorizontalHeaderLabels(["Fecha", "Tipo", "Monto", "Lugar"])
        self.tabla_multas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_multas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_multas.verticalHeader().setVisible(False)
        self.tabla_multas.setMinimumHeight(130)  # 👈 Evita que se aplaste

        self.layout_info.addWidget(self.tabla_multas)

        # 🔥 Separación visual real
        self.layout_info.addSpacing(20)

        linea = QLabel()
        linea.setFixedHeight(1)
        linea.setStyleSheet("background-color:#444; margin-top:10px; margin-bottom:10px;")
        self.layout_info.addWidget(linea)

        # ===== HISTORIAL =====
        titulo_historial = QLabel("HISTORIAL DE CAMBIOS")
        titulo_historial.setStyleSheet("font-size:16px; font-weight:bold; margin-top:5px;")
        self.layout_info.addWidget(titulo_historial)

        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(2)
        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "Cambio"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_historial.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_historial.verticalHeader().setVisible(False)
        self.tabla_historial.setMinimumHeight(160)  # 👈 Hace que respire

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
            layout_principal.setContentsMargins(40, 20, 40, 20)

            # Stack interno para las multas
            self.stack_multas = QStackedWidget()
            layout_principal.addWidget(self.stack_multas)

            # -----------------------------------------------------
            # PASO 1: BUSCAR PLACA PARA MULTAR
            # -----------------------------------------------------
            buscar_widget = QWidget()
            buscar_layout = QVBoxLayout(buscar_widget)
            
            titulo_b = QLabel("REGISTRAR NUEVA MULTA")
            titulo_b.setStyleSheet("font-size: 18px; font-weight: bold;")
            titulo_b.setAlignment(Qt.AlignCenter)

            sub_b = QLabel("Ingrese la placa del vehículo a sancionar")
            sub_b.setAlignment(Qt.AlignCenter)

            self.input_placa_multa = QLineEdit()
            self.input_placa_multa.setPlaceholderText("Ej: DEF456")
            self.input_placa_multa.setMaximumWidth(400)

            btn_validar = QPushButton("Continuar")
            btn_validar.setMinimumHeight(45)
            btn_validar.clicked.connect(self.validar_vehiculo_multa)

            buscar_layout.addStretch()
            buscar_layout.addWidget(titulo_b)
            buscar_layout.addWidget(sub_b)
            buscar_layout.addSpacing(10)
            buscar_layout.addWidget(self.input_placa_multa, alignment=Qt.AlignCenter)
            buscar_layout.addWidget(btn_validar, alignment=Qt.AlignCenter)
            buscar_layout.addStretch()

            self.stack_multas.addWidget(buscar_widget)

            # -----------------------------------------------------
            # PASO 2: FORMULARIO DE MULTA
            # -----------------------------------------------------
            self.form_multa_scroll = self.crear_formulario_multa()
            self.stack_multas.addWidget(self.form_multa_scroll)

            self.stack.addWidget(widget)

    
    def crear_formulario_multa(self):
    
        # Usamos QScrollArea para mantener consistencia con Registrar/Editar
            contenedor_scroll = QScrollArea()
            contenedor_scroll.setWidgetResizable(True)
            
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(80, 30, 80, 30)
            layout.setSpacing(18)
            layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            titulo = QLabel("Detalles de la Infracción")
            titulo.setStyleSheet("font-size: 26px; font-weight: bold;")
            
            layout.addWidget(titulo)
            layout.addSpacing(15)

            self.campos_multa = {}
            campos = [
                ("Placa del Vehículo", "placa"),
                ("Fecha (DD/MM/AAAA)", "fecha"),
                ("Tipo de Infracción", "tipo"),
                ("Monto ($)", "monto"),
                ("Lugar de los hechos", "lugar")
            ]

            for texto, key in campos:
                # Reutilizamos la lógica visual de bloques que tienes
                bloque = QWidget()
                bl_layout = QVBoxLayout(bloque)
                bl_layout.setSpacing(6)
                
                label = QLabel(texto)
                label.setStyleSheet("font-weight: bold;")
                
                entrada = QLineEdit()
                entrada.setMinimumHeight(38)
                entrada.setMaximumWidth(500)
                
                bl_layout.addWidget(label)
                bl_layout.addWidget(entrada)
                layout.addWidget(bloque)
                
                self.campos_multa[key] = entrada

            # El campo placa debe ser solo lectura porque ya lo buscamos
            self.campos_multa["placa"].setReadOnly(True)
            self.campos_multa["placa"].setStyleSheet("color: #888; border-bottom: 1px solid #333;")

            btn_guardar = QPushButton("Registrar Multa")
            btn_guardar.setMinimumHeight(45)
            btn_guardar.setMaximumWidth(300)
            btn_guardar.clicked.connect(self.procesar_registro_multa)

            btn_cancelar = QPushButton("Cancelar")
            btn_cancelar.setMaximumWidth(300)
            btn_cancelar.clicked.connect(lambda: self.stack_multas.setCurrentIndex(0))
            
            layout.addWidget(btn_guardar)
            layout.addWidget(btn_cancelar)
            layout.addStretch()

            contenedor_scroll.setWidget(widget)
            return contenedor_scroll

        # --- FUNCIONES LÓGICAS PARA MULTAS ---

    def validar_vehiculo_multa(self):
            placa = self.input_placa_multa.text().strip().upper()
            vehiculo = vehiculos.buscar_por_placa(placa)

            if vehiculo:
                # Llenar el campo placa automáticamente
                self.campos_multa["placa"].setText(placa)
                # Poner fecha actual por defecto
                self.campos_multa["fecha"].setText(datetime.now().strftime("%d/%m/%Y"))
                
                self.stack_multas.setCurrentIndex(1)
                self.form_multa_scroll.verticalScrollBar().setValue(0) # Reset scroll
            else:
                QMessageBox.warning(self, "No encontrado", "No existe un vehículo con esa placa.")

    def procesar_registro_multa(self):
            placa = self.campos_multa["placa"].text()
            fecha = self.campos_multa["fecha"].text()
            tipo = self.campos_multa["tipo"].text()
            monto = self.campos_multa["monto"].text()
            lugar = self.campos_multa["lugar"].text()

            if not all([fecha, tipo, monto, lugar]):
                QMessageBox.warning(self, "Campos incompletos", "Por favor llena todos los datos.")
                return

            exito, mensaje = vehiculos.agregar_multa(placa, fecha, tipo, monto, lugar)
            
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                # Limpiar y volver
                for c in self.campos_multa.values(): c.clear()
                self.input_placa_multa.clear()
                self.stack_multas.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", mensaje)

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

            # 1. Llenar Labels (Datos Generales)
            for clave, label in self.labels_info.items():
                valor = vehiculo.get(clave, "—")
                texto_base = label.text().split(":")[0]
                label.setText(f"{texto_base}: {valor}")

            # 2. Llenar Tabla de Multas
            self.tabla_multas.setRowCount(0) # Limpiar tabla anterior
            lista_multas = vehiculo.get("multas", [])
            
            for m in lista_multas:
                row = self.tabla_multas.rowCount()
                self.tabla_multas.insertRow(row)
                
                # Aseguramos que existan las claves, si no, pone string vacío
                fecha = m.get("fecha", "")
                tipo = m.get("tipo_infraccion", "")
                monto = f"${m.get('monto', '0')}"
                lugar = m.get("lugar", "")

                self.tabla_multas.setItem(row, 0, QTableWidgetItem(fecha))
                self.tabla_multas.setItem(row, 1, QTableWidgetItem(tipo))
                self.tabla_multas.setItem(row, 2, QTableWidgetItem(monto))
                self.tabla_multas.setItem(row, 3, QTableWidgetItem(lugar))

            # 3. Llenar Tabla de Historial
            self.tabla_historial.setRowCount(0) # Limpiar tabla anterior
            lista_historial = vehiculo.get("historial", [])
            
            # Invertimos la lista para ver lo más reciente arriba (opcional, pero recomendado)
            for h in reversed(lista_historial):
                row = self.tabla_historial.rowCount()
                self.tabla_historial.insertRow(row)

                # Tu backend ya normaliza esto, así que siempre debería ser diccionario
                if isinstance(h, dict):
                    fecha = h.get("fecha", "")
                    cambio = h.get("cambio", "")
                else:
                    # Fallback por si acaso queda algún string viejo
                    fecha = "—"
                    cambio = str(h)

                self.tabla_historial.setItem(row, 0, QTableWidgetItem(fecha))
                self.tabla_historial.setItem(row, 1, QTableWidgetItem(cambio))
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