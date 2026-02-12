"""
Módulo de Lógica de Negocio y Persistencia de Datos.

Este archivo actúa como el backend de la aplicación. Se encarga de:
1. Gestionar la persistencia de datos en un archivo JSON local (datos.json).
2. Realizar validaciones de negocio (ej. unicidad de placas).
3. Proveer funciones CRUD (Crear, Leer, Actualizar, Borrar -aunque no borramos, cambiamos estado-).
4. Administrar el historial de cambios y el registro de multas.

No contiene código de interfaz gráfica (PySide6)
"""

import json
import os
from datetime import datetime

# Configuración de rutas para persistencia de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE_DIR, "datos.json")

# ===============================
# MANEJO DE ARCHIVO
# ===============================

def cargar_datos():
    """
    Lee los datos desde el archivo JSON especificado.
    
    Si el archivo no existe, retorna una lista vacía.
    Realiza una normalización de la estructura de datos para asegurar
    que todos los registros tengan los campos 'multas' e 'historial'.
    También migra formatos antiguos de historial (cadenas de texto)
    al nuevo formato de diccionarios.

    Returns:
        list: Una lista de diccionarios representando los vehículos.
    """
    if not os.path.exists(ARCHIVO_DATOS):
        return []

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            vehiculos = json.load(archivo)

        # Normalizar estructura de datos
        datos_modificados = False
        for v in vehiculos:
            if "multas" not in v:
                v["multas"] = []
                datos_modificados = True
            if "historial" not in v:
                v["historial"] = []
                datos_modificados = True

            # Conversión de historial antiguo (str) a nuevo formato (dict)
            nuevo_historial = []
            historial_cambiado = False
            for h in v["historial"]:
                if isinstance(h, str):
                    historial_cambiado = True
                    if " - " in h:
                        fecha, cambio = h.split(" - ", 1)
                        nuevo_historial.append({"fecha": fecha, "cambio": cambio})
                    else:
                        nuevo_historial.append({"fecha": "", "cambio": h})
                else:
                    nuevo_historial.append(h)

            if historial_cambiado:
                v["historial"] = nuevo_historial
                datos_modificados = True

        # Guardar cambios estructurales si hubo migraciones
        if datos_modificados:
            guardar_datos(vehiculos)

        return vehiculos

    except (json.JSONDecodeError, IOError):
        return []


def guardar_datos(lista_vehiculos):
    """
    Escribe la lista de vehículos en el archivo JSON.

    Args:
        lista_vehiculos (list): Lista de diccionarios con datos de vehículos.
    """
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(lista_vehiculos, archivo, indent=4, ensure_ascii=False)


# ===============================
# GESTIÓN DE VEHÍCULOS (CRUD)
# ===============================

def registrar_vehiculo(datos):
    """
    Registra un nuevo vehículo en el sistema.

    Valida que la placa no exista previamente y que el año sea numérico.
    Inicializa los campos de estado, historial y multas.

    Args:
        datos (dict): Diccionario con los datos del formulario (placa, marca, etc.).

    Returns:
        tuple: (bool, str) indicando éxito/fallo y un mensaje descriptivo.
    """
    vehiculos = cargar_datos()

    datos["placa"] = str(datos["placa"]).strip().upper()

    if any(v["placa"] == datos["placa"] for v in vehiculos):
        return False, "La placa ya está registrada."

    if not str(datos["anio"]).isdigit():
        return False, "El año debe ser numérico."

    datos["anio"] = str(datos["anio"])
    datos["estado"] = "Activo"
    datos["historial"] = []
    datos["multas"] = []

    vehiculos.append(datos)
    guardar_datos(vehiculos)

    return True, "Vehículo registrado correctamente."


def buscar_por_placa(placa):
    """
    Busca un vehículo específico por su número de placa.

    Args:
        placa (str): La placa a buscar.

    Returns:
        dict | None: El diccionario del vehículo si se encuentra, o None si no existe.
    """
    vehiculos = cargar_datos()
    placa = str(placa).strip().upper()

    for v in vehiculos:
        if str(v.get("placa", "")).strip().upper() == placa:
            return v

    return None


def editar_vehiculo(placa, nuevos_datos):
    """
    Actualiza la información de un vehículo existente.

    No permite modificar la placa ni sobreescribir directamente el historial
    o las multas desde esta función. Registra el cambio en el historial.

    Args:
        placa (str): Identificador del vehículo a editar.
        nuevos_datos (dict): Diccionario con las claves y valores a actualizar.

    Returns:
        tuple: (bool, str) indicando éxito/fallo y un mensaje descriptivo.
    """
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            for clave in nuevos_datos:
                # Evita sobreescribir campos protegidos
                if clave in v and clave not in ["placa", "historial", "multas"]:
                    v[clave] = nuevos_datos[clave]

            agregar_historial(v, "Datos del vehículo modificados")
            guardar_datos(vehiculos)
            return True, "Vehículo actualizado."

    return False, "Vehículo no encontrado."


def cambiar_estado(placa, nuevo_estado):
    """
    Modifica el estado (ej. Activo, Reportado) de un vehículo.

    Args:
        placa (str): Identificador del vehículo.
        nuevo_estado (str): El nuevo estado a asignar.

    Returns:
        tuple: (bool, str) indicando éxito/fallo y un mensaje descriptivo.
    """
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            v["estado"] = nuevo_estado
            agregar_historial(v, f"Estado cambiado a {nuevo_estado}")
            guardar_datos(vehiculos)
            return True, "Estado actualizado."

    return False, "Vehículo no encontrado."


def listar_vehiculos(filtro=None):
    """
    Obtiene la lista de vehículos registrados.

    Args:
        filtro (str, opcional): Estado por el cual filtrar (ej. "Activo"). 
                                Si es None, devuelve todos.

    Returns:
        list: Lista de diccionarios de vehículos.
    """
    vehiculos = cargar_datos()

    if filtro is None:
        return vehiculos

    return [v for v in vehiculos if v["estado"] == filtro]


# ===============================
# GESTIÓN DE HISTORIAL Y MULTAS
# ===============================

def agregar_historial(vehiculo, evento):
    """
    Agrega una entrada al historial del vehículo con la fecha actual.
    
    Esta función modifica el diccionario del vehículo 'in-place'.

    Args:
        vehiculo (dict): El diccionario del vehículo a modificar.
        evento (str): Descripción del evento a registrar.
    """
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    vehiculo["historial"].append({
        "fecha": fecha,
        "cambio": evento
    })


def agregar_multa(placa, fecha, tipo, monto, lugar):
    """
    Registra una nueva multa a un vehículo.

    Args:
        placa (str): Identificador del vehículo.
        fecha (str): Fecha de la infracción.
        tipo (str): Tipo de infracción.
        monto (str/float): Monto de la multa.
        lugar (str): Lugar donde ocurrió la infracción.

    Returns:
        tuple: (bool, str) indicando éxito/fallo y un mensaje descriptivo.
    """
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            multa = {
                "fecha": fecha,
                "tipo_infraccion": tipo, 
                "monto": monto,           
                "lugar": lugar
            }

            v["multas"].append(multa)
            agregar_historial(v, f"Multa registrada: {tipo} por ${monto}")
            guardar_datos(vehiculos)
            return True, "Multa agregada correctamente."

    return False, "Vehículo no encontrado."


def contar_multas(placa):
    """
    Cuenta el número total de multas asociadas a una placa.

    Args:
        placa (str): Identificador del vehículo.

    Returns:
        int: Cantidad de multas registradas (0 si el vehículo no existe).
    """
    vehiculos = cargar_datos()

    for v in vehiculos:
        if v["placa"] == placa:
            return len(v["multas"])

    return 0