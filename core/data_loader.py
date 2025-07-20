import pandas as pd
from datetime import datetime

def cargar_datos(resumen_path='resources/RESUMEN CLIENTE.xlsx', accesos_path='resources/ACCESOS.xlsx'):
    # Leer Excel de clientes
    resumen_df = pd.read_excel(resumen_path)
    accesos_df = pd.read_excel(accesos_path)

    # Limpiar y convertir fechas
    resumen_df["Inicio del abono"] = pd.to_datetime(resumen_df["Inicio del abono"], errors="coerce")
    resumen_df["Fecha de nacimiento"] = pd.to_datetime(resumen_df["Fecha de nacimiento"], errors="coerce")
    accesos_df["Fecha de acceso"] = pd.to_datetime(accesos_df["Fecha de acceso"], errors="coerce")

    # Calcular días desde alta y edad
    hoy = pd.Timestamp.today().normalize()
    resumen_df["Días desde alta"] = (hoy - resumen_df["Inicio del abono"]).dt.days

    def calcular_edad(nacimiento):
        if pd.notnull(nacimiento):
            return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return None

    resumen_df["Edad"] = resumen_df["Fecha de nacimiento"].apply(calcular_edad)

    # Asignar sexo según codificación real de Resamania
    resumen_df["Sexo"] = resumen_df["Civilidad"].map({
        "Mr": "Masculino",
        "Mme": "Femenino"
    }).fillna("Desconocido")

    return resumen_df, accesos_df
