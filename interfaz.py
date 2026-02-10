from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
import vehiculos


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Control Vehicular")
        self.setGeometry(200, 50, 600, 700)

        # 📦 Contenedor principal
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout = QVBoxLayout(contenedor)

        # 🧾 Formulario datos vehículo
        form = QFormLayout()
        layout.addLayout(form)

        self.campos = {}
        labels = ["placa", "marca", "modelo", "año", "color", "tipo", "propietario", "telefono"]

        for label in labels:
            entrada = QLineEdit()
            self.campos[label] = entrada
            form.addRow(label.capitalize(), entrada)

        # 🚨 Multas
        self.entry_fecha = QLineEdit()
        self.entry_num_multas = QLineEdit()
        self.entry_corralon = QLineEdit()
        self.entry_lugar = QLineEdit()

        form.addRow("Fecha multa", self.entry_fecha)
        form.addRow("# Multas persona", self.entry_num_multas)
        form.addRow("¿Corralón?", self.entry_corralon)
        form.addRow("Lugar multa", self.entry_lugar)

        # 📄 Área de resultados
        self.resultado = QTextEdit()
        layout.addWidget(self.resultado)

        # 🔘 Botones
        botones = [
            ("Registrar Vehículo", self.registrar),
            ("Buscar Vehículo", self.buscar),
            ("Editar Vehículo", self.editar),
            ("Cambiar Estado", self.cambiar_estado),
            ("Listar Vehículos", self.listar),
            ("Registrar Multa", self.registrar_multa)
        ]

        for texto, funcion in botones:
            boton = QPushButton(texto)
            boton.clicked.connect(funcion)
            layout.addWidget(boton)

    # ================= FUNCIONES =================

    def registrar(self):
        datos = {k: v.text() for k, v in self.campos.items()}
        datos["placa"] = datos["placa"].upper()

        if any(x.strip() == "" for x in datos.values()):
            QMessageBox.critical(self, "Error", "Todos los campos son obligatorios")
            return

        exito, mensaje = vehiculos.registrar_vehiculo(datos)
        QMessageBox.information(self, "Resultado", mensaje)

        if exito:
            for v in self.campos.values():
                v.clear()

    def buscar(self):
        placa = self.campos["placa"].text().strip().upper()

        if placa == "":
            QMessageBox.critical(self, "Error", "Ingresa una placa")
            
        vehiculo = vehiculos.buscar_por_placa(placa)
        self.resultado.clear()

        if not vehiculo:
            QMessageBox.critical(self, "Error", "Vehículo no encontrado")
            return

        info = ""
        for k, v in vehiculo.items():
            if k not in ["historial", "multas"]:
                info += f"{k.capitalize()}: {v}\n"

        info += "\nHistorial:\n"
        if vehiculo["historial"]:
            for h in vehiculo["historial"]:
                info += f"- {h}\n"
        else:
            info += "Sin registros\n"

        info += "\nMultas:\n"
        if vehiculo["multas"]:
            for m in vehiculo["multas"]:
                info += f"- {m['fecha']} | {m['lugar']} | Corralón: {m['corralon']} | Multas persona: {m['numero_multas']}\n"
        else:
            info += "Sin multas\n"
            
        self.resultado.setText(info)

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
        self.resultado.clear()

        for v in lista:
            self.resultado.append(f"{v['placa']} | {v['marca']} {v['modelo']} | {v['estado']}")

    def registrar_multa(self):
        placa = self.campos["placa"].text()
        fecha = self.entry_fecha.text()
        num = self.entry_num_multas.text()
        corralon = self.entry_corralon.text()
        lugar = self.entry_lugar.text()

        exito, mensaje = vehiculos.agregar_multa(placa, fecha, num, corralon, lugar)
        QMessageBox.information(self, "Resultado", mensaje)
