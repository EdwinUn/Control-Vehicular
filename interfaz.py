import tkinter as tk
from tkinter import messagebox
import vehiculos


def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Sistema de Control Vehicular")
    ventana.geometry("500x500")

    # =========================
    # 🧾 CAMPOS DEL FORMULARIO
    # =========================
    labels = [
        "Placa", "Marca", "Modelo", "Año",
        "Color", "Tipo", "Propietario", "Teléfono"
    ]

    entradas = {}

    for i, texto in enumerate(labels):
        label = tk.Label(ventana, text=texto)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(ventana, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entradas[texto.lower()] = entry

    tk.Label(ventana, text="Fecha multa").grid(row=14, column=0)
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=14, column=1)

    tk.Label(ventana, text="# Multas persona").grid(row=15, column=0)
    entry_num_multas = tk.Entry(ventana)
    entry_num_multas.grid(row=15, column=1)

    tk.Label(ventana, text="¿Corralón? (Sí/No)").grid(row=16, column=0)
    entry_corralon = tk.Entry(ventana)
    entry_corralon.grid(row=16, column=1)

    tk.Label(ventana, text="Lugar multa").grid(row=17, column=0)
    entry_lugar = tk.Entry(ventana)
    entry_lugar.grid(row=17, column=1)

    # =========================
    # 🚗 FUNCIÓN REGISTRAR
    # =========================
    def registrar():
        datos = {
            "placa": entradas["placa"].get(),
            "marca": entradas["marca"].get(),
            "modelo": entradas["modelo"].get(),
            "año": entradas["año"].get(),
            "color": entradas["color"].get(),
            "tipo": entradas["tipo"].get(),
            "propietario": entradas["propietario"].get(),
            "telefono": entradas["teléfono"].get()
        }

        # Validar campos vacíos
        if any(valor.strip() == "" for valor in datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        exito, mensaje = vehiculos.registrar_vehiculo(datos)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            for campo in entradas.values():
                campo.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
    
    def buscar():
        placa = entradas["placa"].get().strip()

        if placa == "":
            messagebox.showerror("Error", "Dato incorrecto.")
            return

        vehiculo = vehiculos.buscar_por_placa(placa)

        resultado_texto.delete("1.0", tk.END)

        if vehiculo:
            info = ""
            for clave, valor in vehiculo.items():
                if clave != "historial":
                    info += f"{clave.capitalize()}: {valor}\n"

            info += "\nHistorial:\n"
            if vehiculo["historial"]:
                for evento in vehiculo["historial"]:
                    info += f"- {evento}\n"
            else:
                info += "Sin registros\n"

            resultado_texto.insert(tk.END, info)
        else:
            messagebox.showerror("Error", "Vehículo no encontrado.")
            
    def editar():
        placa = entradas["placa"].get().strip()

        if placa == "":
            messagebox.showerror("Error", "Ingresa la placa del vehículo a editar.")
            return

        nuevos_datos = {
            "marca": entradas["marca"].get(),
            "modelo": entradas["modelo"].get(),
            "año": entradas["año"].get(),
            "color": entradas["color"].get(),
            "tipo": entradas["tipo"].get(),
            "propietario": entradas["propietario"].get(),
            "telefono": entradas["teléfono"].get()
        }

        exito, mensaje = vehiculos.editar_vehiculo(placa, nuevos_datos)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
        
    def cambiar_estado():
        placa = entradas["placa"].get().strip()

        if placa == "":
            messagebox.showerror("Error", "Ingresa la placa.")
            return

        # Ventana pequeña para elegir estado
        ventana_estado = tk.Toplevel()
        ventana_estado.title("Cambiar Estado")

        tk.Label(ventana_estado, text="Selecciona el nuevo estado").pack(pady=10)

        estados = ["Activo", "Baja", "Reportado"]
        estado_var = tk.StringVar(value="Activo")

        for e in estados:
            tk.Radiobutton(ventana_estado, text=e, variable=estado_var, value=e).pack(anchor="w")

        def confirmar():
            exito, mensaje = vehiculos.cambiar_estado(placa, estado_var.get())
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_estado.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(ventana_estado, text="Confirmar", command=confirmar).pack(pady=10)
        
    def listar():
        lista = vehiculos.listar_vehiculos()
        resultado_texto.delete("1.0", tk.END)

        if not lista:
            resultado_texto.insert(tk.END, "No hay vehículos registrados.")
            return

        for v in lista:
            resultado_texto.insert(
                tk.END,
                f"{v['placa']} | {v['marca']} {v['modelo']} | {v['estado']}\n"
            )
  
    # =========================
    # 🔘 BOTÓN
    # =========================
    boton_registrar = tk.Button(
        ventana, text="Registrar Vehículo", command=registrar, width=20, bg="#4CAF50", fg="white"
    )
    boton_registrar.grid(row=len(labels), column=0, columnspan=2, pady=20)
    
    resultado_texto = tk.Text(ventana, height=10, width=55)
    resultado_texto.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    resultado_texto = tk.Text(ventana, height=10, width=55)
    resultado_texto.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    boton_buscar = tk.Button(
    ventana, text="Buscar Vehículo", command=buscar, width=20, bg="#2196F3", fg="white")
    boton_buscar.grid(row=9, column=0, columnspan=2, pady=5)

    boton_editar = tk.Button(
    ventana, text="Editar Vehículo", command=editar, width=20, bg="#FF9800", fg="white")
    boton_editar.grid(row=11, column=0, columnspan=2, pady=5)

    boton_estado = tk.Button(
    ventana, text="Cambiar Estado", command=cambiar_estado, width=20, bg="#9C27B0", fg="white")
    boton_estado.grid(row=12, column=0, columnspan=2, pady=5)

    boton_listar = tk.Button(
    ventana, text="Listar Vehículos", command=listar, width=20, bg="#607D8B", fg="white")
    boton_listar.grid(row=13, column=0, columnspan=2, pady=5)

    ventana.mainloop()
