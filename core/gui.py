import tkinter as tk
from tkinter import filedialog, ttk, font, Menu

def mostrar_clientes(clientes_df, cargar_callback, root, ruta_actual=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1200x700")
    root.minsize(1000, 600)

    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 11))
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    frame_superior = tk.Frame(root)
    frame_superior.pack(padx=20, pady=10, fill="x")

    instrucciones = tk.Label(
        frame_superior,
        text=(
            "🟡  INSTRUCCIONES PARA USO CORRECTO 🟡\n\n"
            "➡️  La carpeta seleccionada debe contener estos dos archivos renombrados así:\n\n"
            "    ✔️  RESUMEN CLIENTE.xlsx (exportado de resamania)\n"
            "    ✔️  ACCESOS.xlsx (exportado también de resemania seleccionando intervalo de fechas de últimas 4 semanas)\n\n"
            "📅  Ambos archivos deben estar actualizados y corresponder al mismo día de exportación.\n\n"
            "➡️  Pulsa el botón 'Seleccionar carpeta' para comenzar la revisión.\n\n"
            "🟡  NOTA: UNA VEZ SELECCINADA CARPETA, EL PROGRAMA LA MANTIENE POR DEFECTO HASTA QUE SE SELECCIONE OTRA 🟡"
        ),
        font=("Segoe UI", 12),
        justify="left",
        anchor="w"
    )
    instrucciones.pack(pady=10)

    btn_carpeta = ttk.Button(frame_superior, text="📂 Seleccionar carpeta", command=lambda: seleccionar_ruta(cargar_callback))
    btn_carpeta.pack(pady=5)

    if ruta_actual:
        btn_actualizar = ttk.Button(frame_superior, text="🔄 Actualizar datos", command=lambda: cargar_callback(ruta_actual))
        btn_actualizar.pack(pady=5)

    if clientes_df is not None and not clientes_df.empty:
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(frame_tabla, show="headings")
        tree["columns"] = list(clientes_df.columns)

        vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        orden_estado = {col: False for col in clientes_df.columns}

        def ordenar_columna(col):
            orden = not orden_estado[col]
            orden_estado[col] = orden
            df_ordenado = clientes_df[clientes_df[col].notna()].sort_values(by=col, ascending=orden)
            tree.delete(*tree.get_children())
            for _, row in df_ordenado.iterrows():
                valores = [formatear_valor(row[c]) for c in tree["columns"]]
                tree.insert("", "end", values=valores)

        def formatear_valor(valor):
            if isinstance(valor, float) and valor.is_integer():
                return str(int(valor))
            return str(valor)

        for col in clientes_df.columns:
            tree.heading(col, text=col, command=lambda c=col: ordenar_columna(c))
            tree.column(col, anchor="center", width=130)

        for _, row in clientes_df.iterrows():
            valores = [formatear_valor(row[c]) for c in tree["columns"]]
            tree.insert("", "end", values=valores)

        # --------- COPIAR CELDA --------- #
        def copiar_celda(event=None):
            item_id = tree.focus()
            if not item_id:
                return
            col = tree.identify_column(event.x if event else tree.winfo_pointerx() - tree.winfo_rootx())
            col_index = int(col.replace('#', '')) - 1
            valor = tree.item(item_id)['values'][col_index]
            root.clipboard_clear()
            root.clipboard_append(valor)

        def doble_click(event):
            copiar_celda(event)

        def copiar_con_ctrl_c(event):
            copiar_celda()

        def mostrar_menu_contextual(event):
            item_id = tree.identify_row(event.y)
            if item_id:
                tree.selection_set(item_id)
                menu = Menu(tree, tearoff=0)
                menu.add_command(label="Copiar", command=lambda: copiar_celda(event))
                menu.tk_popup(event.x_root, event.y_root)

        tree.bind("<Double-1>", doble_click)
        tree.bind("<Control-c>", copiar_con_ctrl_c)
        tree.bind("<Button-3>", mostrar_menu_contextual)  # botón derecho

def seleccionar_ruta(cargar_callback):
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos Excel")
    if carpeta:
        cargar_callback(carpeta)
