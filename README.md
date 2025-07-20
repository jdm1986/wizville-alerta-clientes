# 🟡 Wizville Alerta Clientes

Este programa ha sido desarrollado por **JDM Developer** para automatizar la detección diaria de clientes que deben recibir una encuesta de Wizville.  
Analiza los ficheros exportados desde Resamania y determina en función de la antigüedad y los accesos, quiénes cumplen los criterios.

## 📂 Requisitos

Coloca en la misma carpeta los siguientes archivos exportados desde Resamania:

- `RESUMEN CLIENTE.xlsx`
- `ACCESOS.xlsx` (último mes de accesos)

Ambos archivos deben tener la **misma fecha de exportación**.

## 🧠 Funcionalidad

El programa detecta automáticamente:

- Clientes con **16 días** o **180 días** desde la inscripción.
- Su franja horaria más frecuente de entrenamiento.
- Visualización interactiva y ordenable.
- Posibilidad de cambiar de carpeta y actualizar los datos en vivo.

## 🖥️ Interfaz

- Interfaz gráfica desarrollada con `Tkinter`.
- Tabla con scroll, ordenable por cualquier columna.
- Botones para selección de carpeta y actualización de datos.
- Memoria de la última carpeta utilizada.

## ▶️ Ejecución

```bash
python main.py
