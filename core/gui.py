import tkinter as tk
from tkinter import filedialog, ttk, font

def mostrar_clientes(clientes_df, cargar_callback, root, ruta_actual=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1200x700")
    root.minsize(1000, 600)

    # Estilos para Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    # Frame superior para instrucciones y botones
    frame_superior = tk.Frame(root)
    frame_superior.pack(padx=20, pady=10, fill="x")

    instrucciones = tk.Label(
        frame_superior,
        text=(
            "🟡  INSTRUCCIONES PARA USO CORRECTO 🟡\n\n"
            "1️⃣  Asegúrate de que la carpeta contiene los dos archivos siguientes:\n"
            "    ✔️  RESUMEN CLIENTE.xlsx\n"
            "    ✔️  ACCESOS.xlsx (exportado con accesos del último mes)\n\n"
            "📅  Ambos archivos deben estar actualizados y corresponder al mismo día.\n\n"
            "➡️  Pulsa el botón 'Seleccionar carpeta' para comenzar la revisión."
        ),
        font=("Segoe UI", 12),
        justify="left",
        anchor="w"
    )
    instrucciones.pack(pady=10)

    # Botón para seleccionar nueva carpeta
    btn_carpeta = ttk.Button(frame_superior, text="📂 Seleccionar carpeta", command=lambda: seleccionar_ruta(cargar_callback))
    btn_carpeta.pack(pady=5)

    # Botón para recargar datos desde la carpeta actual
    if ruta_actual:
        btn_actualizar = ttk.Button(frame_superior, text="🔄 Actualizar datos", command=lambda: cargar_callback(ruta_actual))
        btn_actualizar.pack(pady=5)

    # Tabla de clientes
    if clientes_df is not None and not clientes_df.empty:
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(frame_tabla, show="headings")
        tree["columns"] = list(clientes_df.columns)

        # Scrollbars
        vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        # Ordenamiento por columna
        orden_estado = {col: False for col in clientes_df.columns}

        def ordenar_columna(col):
            no_na_df = clientes_df[clientes_df[col].notna()]
            orden = not orden_estado[col]
            orden_estado[col] = orden
            df_ordenado = no_na_df.sort_values(by=col, ascending=orden)
            tree.delete(*tree.get_children())
            for _, row in df_ordenado.iterrows():
                tree.insert("", "end", values=list(row))

        for col in clientes_df.columns:
            tree.heading(col, text=col, command=lambda c=col: ordenar_columna(c))
            tree.column(col, anchor="center", width=130)

        for _, row in clientes_df.iterrows():
            tree.insert("", "end", values=list(row))


def seleccionar_ruta(cargar_callback):
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos Excel")
    if carpeta:
        cargar_callback(carpeta)
