import tkinter as tk
from tkinter import messagebox
import random

# ---------------- BASE DE DATOS ----------------

vehiculos = {
    "ABC123": {"propietario": "Juan Perez", "robado": False},
    "XYZ789": {"propietario": "Maria Lopez", "robado": True},
    "LMN456": {"propietario": "Carlos Ruiz", "robado": False}
}

# ---------------- FUNCIONES ----------------

def buscar_vehiculo():
    placas = entry_placas.get().upper()

    if placas in vehiculos:
        info = vehiculos[placas]
        texto = f"Placas: {placas}\n"
        texto += f"Propietario: {info['propietario']}\n"

        if info["robado"]:
            texto += "🚨 VEHÍCULO REPORTADO COMO ROBADO"
            messagebox.showerror("Alerta", texto)
        else:
            texto += "✅ Vehículo sin reporte de robo"
            messagebox.showinfo("Resultado", texto)
    else:
        messagebox.showwarning("No encontrado", "Vehículo no registrado")

def cambiar_propietario():
    placas = entry_placas.get().upper()
    nuevo = entry_nuevo_prop.get()

    if placas in vehiculos:
        if nuevo == "":
            messagebox.showerror("Error", "Ingresa el nuevo propietario")
            return

        vehiculos[placas]["propietario"] = nuevo
        messagebox.showinfo(
            "Éxito",
            f"Propietario actualizado\nPlacas: {placas}\nNuevo dueño: {nuevo}"
        )
    else:
        messagebox.showerror("Error", "Vehículo no encontrado")

def control_vehicular():
    placas = entry_placas.get().upper()

    if placas not in vehiculos:
        messagebox.showerror("Error", "Primero busca un vehículo válido")
        return

    if vehiculos[placas]["robado"]:
        messagebox.showerror("Detención", "🚔 Vehículo robado. Proceder a aseguramiento.")
        return

    alcohol = random.randint(0, 100)

    resultado = f"Placas: {placas}\n"
    resultado += f"Alcoholímetro: {alcohol}\n\n"

    if var_licencia.get() == 0:
        resultado += "❌ Sin licencia\n"
    if var_tarjeta.get() == 0:
        resultado += "❌ Sin tarjeta de circulación\n"
    if var_cinturon.get() == 0:
        resultado += "❌ No usa cinturón\n"
    if alcohol > 60:
        resultado += "❌ Exceso de alcohol\n"

    if (var_licencia.get() == 1 and var_tarjeta.get() == 1
        and var_cinturon.get() == 1 and alcohol <= 60):
        resultado += "\n✅ Puede continuar"
        messagebox.showinfo("Control Vehicular", resultado)
    else:
        resultado += "\n🚫 Multa aplicada"
        messagebox.showwarning("Control Vehicular", resultado)

# ---------------- INTERFAZ ----------------

ventana = tk.Tk()
ventana.title("Sistema de Control Vehicular")
ventana.geometry("450x520")

tk.Label(ventana, text="🚓 CONTROL VEHICULAR 🚓",
         font=("Arial", 16, "bold")).pack(pady=10)

# Placas
tk.Label(ventana, text="Placas del vehículo:").pack()
entry_placas = tk.Entry(ventana)
entry_placas.pack(pady=5)

tk.Button(ventana, text="Buscar Vehículo",
          command=buscar_vehiculo).pack(pady=5)

# Cambio propietario
tk.Label(ventana, text="Nuevo propietario:").pack()
entry_nuevo_prop = tk.Entry(ventana)
entry_nuevo_prop.pack(pady=5)

tk.Button(ventana, text="Cambiar Propietario",
          command=cambiar_propietario).pack(pady=10)

# Control
tk.Label(ventana, text="Revisión del conductor",
         font=("Arial", 12, "bold")).pack(pady=10)

var_licencia = tk.IntVar()
var_tarjeta = tk.IntVar()
var_cinturon = tk.IntVar()

tk.Checkbutton(ventana, text="Licencia vigente",
               variable=var_licencia).pack(anchor="w", padx=50)
tk.Checkbutton(ventana, text="Tarjeta de circulación",
               variable=var_tarjeta).pack(anchor="w", padx=50)
tk.Checkbutton(ventana, text="Usa cinturón",
               variable=var_cinturon).pack(anchor="w", padx=50)

tk.Button(ventana, text="Aplicar Control Vehicular",
          bg="green", fg="white",
          command=control_vehicular).pack(pady=20)

ventana.mainloop()