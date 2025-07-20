import tkinter as tk
from tkinter import messagebox
import os
import json

from core.data_loader import cargar_datos
from core.gui import mostrar_clientes
from core.wizville_logic import calcular_franja_horaria

CONFIG_FILE = "config.json"

def guardar_ruta_config(ruta):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"ruta": ruta}, f)

def obtener_ruta_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("ruta")
    return None

def cargar_y_mostrar(carpeta=None, root=None):
    if not carpeta:
        mostrar_clientes(None, lambda nueva_ruta: cargar_y_mostrar(nueva_ruta, root), root)
        return

    resumen_path = os.path.join(carpeta, "RESUMEN CLIENTE.xlsx")
    accesos_path = os.path.join(carpeta, "ACCESOS.xlsx")

    # Verificar existencia de archivos
    if not os.path.exists(resumen_path) or not os.path.exists(accesos_path):
        msg = "Faltan uno o ambos archivos requeridos en la carpeta seleccionada:\n\n"
        if not os.path.exists(resumen_path):
            msg += "- No se encuentra RESUMEN CLIENTE.xlsx\n"
        if not os.path.exists(accesos_path):
            msg += "- No se encuentra ACCESOS.xlsx\n"
        msg += "\nAsegúrate de que los archivos estén correctamente nombrados."
        messagebox.showerror("Archivos no encontrados", msg, parent=root)
        return

    try:
        resumen, accesos = cargar_datos(resumen_path, accesos_path)
    except Exception as e:
        messagebox.showerror("Error al cargar archivos", str(e), parent=root)
        return

    # Guardar carpeta usada para futuras sesiones
    guardar_ruta_config(carpeta)

    # Filtrado y procesamiento
    clientes_hoy = resumen[resumen["Días desde alta"].isin([16, 180])]
    franjas = calcular_franja_horaria(accesos)
    clientes_hoy = clientes_hoy.merge(franjas, how="left", on="Número de cliente")

    columnas_gui = ["Nombre", "Apellidos", "Número de cliente", "Edad", "Sexo", "Móvil", "Días desde alta", "Franja probable"]
    clientes_filtrados = clientes_hoy[columnas_gui]

    mostrar_clientes(clientes_filtrados, lambda nueva_ruta: cargar_y_mostrar(nueva_ruta, root), root=root, ruta_actual=carpeta)


# Punto de entrada
if __name__ == "__main__":
    root = tk.Tk()
    root.title("PROGRAMA DESARROLLADO POR -- JDM DEVELOPER -- ALERTA CLIENTES CON ENCUESTA WIZVILLE DIARIA")
    root.state("zoomed")  # Ventana maximizada desde el arranque

    ruta_guardada = obtener_ruta_config()
    if ruta_guardada and os.path.exists(os.path.join(ruta_guardada, "RESUMEN CLIENTE.xlsx")) and \
            os.path.exists(os.path.join(ruta_guardada, "ACCESOS.xlsx")):
        cargar_y_mostrar(carpeta=ruta_guardada, root=root)
    else:
        cargar_y_mostrar(carpeta=None, root=root)

    root.mainloop()
