import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE_DIR, "datos.json")

# ===============================
# 📂 MANEJO DE ARCHIVO
# ===============================

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            vehiculos = json.load(archivo)

            for v in vehiculos:
                if "multas" not in v:
                    v["multas"] = []
                if "historial" not in v:
                    v["historial"] = []

            return vehiculos
    except:
        return []


def guardar_datos(lista_vehiculos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(lista_vehiculos, archivo, indent=4, ensure_ascii=False)


# ===============================
# 🚗 REGISTRAR VEHÍCULO
# ===============================

def registrar_vehiculo(datos):
    vehiculos = cargar_datos()

    datos["placa"] = str(datos["placa"]).strip().upper()

    if any(v["placa"] == datos["placa"] for v in vehiculos):
        return False, "La placa ya está registrada."

    # 🔧 CAMBIO AQUÍ → anio SIN Ñ
    if not str(datos["anio"]).isdigit():
        return False, "El año debe ser numérico."

    datos["anio"] = str(datos["anio"])
    datos["estado"] = "Activo"
    datos["historial"] = []
    datos["multas"] = []

    vehiculos.append(datos)
    guardar_datos(vehiculos)

    return True, "Vehículo registrado correctamente."


# ===============================
# 🔍 BUSCAR VEHÍCULO
# ===============================

def buscar_por_placa(placa):
    vehiculos = cargar_datos()
    placa = str(placa).strip().upper()

    for v in vehiculos:
        if str(v.get("placa", "")).strip().upper() == placa:
            return v

    return None


# ===============================
# ✏️ EDITAR VEHÍCULO
# ===============================

def editar_vehiculo(placa, nuevos_datos):
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            for clave in nuevos_datos:
                if clave in v and clave not in ["placa", "historial", "multas"]:
                    v[clave] = nuevos_datos[clave]

            agregar_historial(v, "Datos del vehículo modificados")
            guardar_datos(vehiculos)
            return True, "Vehículo actualizado."

    return False, "Vehículo no encontrado."


# ===============================
# 🔄 CAMBIAR ESTADO
# ===============================

def cambiar_estado(placa, nuevo_estado):
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            v["estado"] = nuevo_estado
            agregar_historial(v, f"Estado cambiado a {nuevo_estado}")
            guardar_datos(vehiculos)
            return True, "Estado actualizado."

    return False, "Vehículo no encontrado."


# ===============================
# 📋 LISTAR VEHÍCULOS
# ===============================

def listar_vehiculos(filtro=None):
    vehiculos = cargar_datos()

    if filtro is None:
        return vehiculos

    return [v for v in vehiculos if v["estado"] == filtro]


# ===============================
# 🧾 HISTORIAL
# ===============================

def agregar_historial(vehiculo, evento):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    vehiculo["historial"].append(f"{fecha} - {evento}")


# ===============================
# 🚨 MULTAS
# ===============================

def agregar_multa(placa, fecha, numero_multas, corralon, lugar):
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            multa = {
                "fecha": fecha,
                "numero_multas": numero_multas,
                "corralon": corralon,
                "lugar": lugar
            }

            v["multas"].append(multa)
            agregar_historial(v, "Se registró una multa")
            guardar_datos(vehiculos)
            return True, "Multa agregada."

    return False, "Vehículo no encontrado."


def contar_multas(placa):
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            return len(v["multas"])

    return 0
