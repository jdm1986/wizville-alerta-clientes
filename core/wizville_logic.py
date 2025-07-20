import pandas as pd
import os
import json

ARCHIVO_RUTA = "ultima_ruta.json"

def calcular_franja_horaria(df_accesos):
    """
    Devuelve un DataFrame con la franja horaria más frecuente por cliente.
    """
    df_accesos = df_accesos.copy()
    df_accesos["Hora"] = df_accesos["Fecha de acceso"].dt.hour

    frecuencias = df_accesos.groupby(["Número de cliente", "Hora"]).size().reset_index(name="frecuencia")
    idx_max = frecuencias.groupby("Número de cliente")["frecuencia"].idxmax()
    franjas = frecuencias.loc[idx_max][["Número de cliente", "Hora"]]
    franjas["Franja probable"] = franjas["Hora"].apply(lambda h: f"{h:02d}:00 - {h+1:02d}:00")

    return franjas[["Número de cliente", "Franja probable"]]


def guardar_ultima_ruta(carpeta):
    try:
        with open(ARCHIVO_RUTA, "w", encoding="utf-8") as f:
            json.dump({"ruta": carpeta}, f)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la ruta: {e}")


def cargar_ultima_ruta():
    try:
        if os.path.exists(ARCHIVO_RUTA):
            with open(ARCHIVO_RUTA, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("ruta")
    except Exception as e:
        print(f"[ERROR] No se pudo leer la última ruta: {e}")
    return None
