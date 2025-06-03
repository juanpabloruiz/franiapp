import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import platform

# ---------- CONEXIÓN A LA BASE DE DATOS ----------
conn = sqlite3.connect('productos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL,
    costo REAL NOT NULL,
    precio REAL NOT NULL,
    fecha TEXT NOT NULL
)
''')
conn.commit()

# ---------- FUNCIONES ----------
def cargar_todos_productos():
    filtro = search_var.get()
    productos = buscar_productos(filtro)
    actualizar_tabla(productos)

def buscar_productos(filtro):
    filtro_like = f"%{filtro}%"
    cursor.execute('''
        SELECT id, codigo, nombre, stock, costo, precio, fecha
        FROM productos
        WHERE codigo LIKE ? OR nombre LIKE ?
    ''', (filtro_like, filtro_like))
    return cursor.fetchall()

def actualizar_tabla(productos):
    for item in tree.get_children():
        tree.delete(item)
    for producto in productos:
        fecha_raw = producto[6]
        # Intentamos parsear fecha guardada en DB para mostrar dd/mm/YYYY
        try:
            fecha_dt = datetime.strptime(fecha_raw, '%Y-%m-%d')
            fecha_fmt = fecha_dt.strftime('%d/%m/%Y')
        except ValueError:
            # Si la fecha no está en formato ISO, la dejamos tal cual
            fecha_fmt = fecha_raw
        producto_mostrar = producto[:6] + (fecha_fmt,)
        tree.insert("", "end", values=producto_mostrar)

def agregar_producto():
    codigo = codigo_var.get()
    nombre = nombre_var.get()
    stock = stock_var.get()
    costo = costo_var.get()
    precio = precio_var.get()
    fecha = fecha_var.get()

    if not (codigo and nombre and fecha):
        messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos")
        return

    try:
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, stock, costo, precio, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, int(stock), float(costo), float(precio), fecha))
        conn.commit()
        cargar_todos_productos()
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar: {e}")

def eliminar_producto():
    item = tree.selection()
    if not item:
        return
    producto_id = tree.item(item)['values'][0]
    cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    cargar_todos_productos()

def actualizar_producto():
    item = tree.selection()
    if not item:
        return
    producto_id = tree.item(item)['values'][0]
    try:
        cursor.execute('''
            UPDATE productos
            SET codigo=?, nombre=?, stock=?, costo=?, precio=?, fecha=?
            WHERE id=?
        ''', (
            codigo_var.get(),
            nombre_var.get(),
            int(stock_var.get()),
            float(costo_var.get()),
            float(precio_var.get()),
            fecha_var.get(),
            producto_id
        ))
        conn.commit()
        cargar_todos_productos()
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar: {e}")

def seleccionar_producto(event):
    item = tree.selection()
    if item:
        datos = tree.item(item)['values']
        codigo_var.set(datos[1])
        nombre_var.set(datos[2])
        stock_var.set(datos[3])
        costo_var.set(datos[4])
        precio_var.set(datos[5])
        # Fecha ya viene en formato dd/mm/YYYY desde la tabla, la ponemos igual en el formulario
        fecha_var.set(datos[6])

def limpiar_campos():
    codigo_var.set("")
    nombre_var.set("")
    stock_var.set(0)
    costo_var.set(0.0)
    precio_var.set(0.0)
    fecha_var.set(datetime.now().strftime('%d/%m/%Y'))

# ---------- INTERFAZ ----------
root = tk.Tk()
root.title("Gestor de Productos")

sistema = platform.system()
if sistema == 'Windows':
    root.state('zoomed')
else:
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    root.geometry(f"{ancho}x{alto}")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(4, weight=1)

# Variables
codigo_var = tk.StringVar()
nombre_var = tk.StringVar()
stock_var = tk.IntVar()
costo_var = tk.DoubleVar()
precio_var = tk.DoubleVar()
fecha_var = tk.StringVar(value=datetime.now().strftime('%d/%m/%Y'))
search_var = tk.StringVar()

# ---------- FORMULARIO ----------
form_frame = ttk.Frame(main_frame)
form_frame.grid(row=0, column=0, sticky="ew", pady=10)
for i in range(7):
    form_frame.columnconfigure(i, weight=1)

ttk.Label(form_frame, text="Código:").grid(row=0, column=0)
ttk.Entry(form_frame, textvariable=codigo_var).grid(row=0, column=1, sticky="ew")

ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2)
ttk.Entry(form_frame, textvariable=nombre_var).grid(row=0, column=3, sticky="ew")

ttk.Label(form_frame, text="Stock:").grid(row=0, column=4)
ttk.Entry(form_frame, textvariable=stock_var).grid(row=0, column=5, sticky="ew")

ttk.Label(form_frame, text="Costo:").grid(row=1, column=0)
ttk.Entry(form_frame, textvariable=costo_var).grid(row=1, column=1, sticky="ew")

ttk.Label(form_frame, text="Precio:").grid(row=1, column=2)
ttk.Entry(form_frame, textvariable=precio_var).grid(row=1, column=3, sticky="ew")

ttk.Label(form_frame, text="Fecha (dd/mm/yyyy):").grid(row=1, column=4)
ttk.Entry(form_frame, textvariable=fecha_var).grid(row=1, column=5, sticky="ew")

# ---------- BOTONES ----------
boton_frame = ttk.Frame(main_frame)
boton_frame.grid(row=1, column=0, sticky="ew", pady=5)
boton_frame.columnconfigure((0,1,2,3), weight=1)

ttk.Button(boton_frame, text="Agregar", command=agregar_producto).grid(row=0, column=0, padx=5, sticky="ew")
ttk.Button(boton_frame, text="Actualizar", command=actualizar_producto).grid(row=0, column=1, padx=5, sticky="ew")
ttk.Button(boton_frame, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5, sticky="ew")
ttk.Button(boton_frame, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5, sticky="ew")

# ---------- BUSCADOR ----------
search_frame = ttk.Frame(main_frame)
search_frame.grid(row=2, column=0, sticky="ew", pady=10)
ttk.Label(search_frame, text="Buscar:").pack(side="left")
tk.Entry(search_frame, textvariable=search_var).pack(side="left", fill="x", expand=True)
# Quité el botón filtrar, busqueda en tiempo real:
def on_search_var_change(*args):
    cargar_todos_productos()
search_var.trace_add("write", on_search_var_change)

# ---------- TABLA ----------
tree = ttk.Treeview(main_frame, columns=("id", "codigo", "nombre", "stock", "costo", "precio", "fecha"), show="headings")
tree.grid(row=4, column=0, sticky="nsew")

for col in ("id", "codigo", "nombre", "stock", "costo", "precio", "fecha"):
    tree.heading(col, text=col.capitalize())

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
scrollbar.grid(row=4, column=1, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

tree.bind("<<TreeviewSelect>>", seleccionar_producto)

# ---------- INICIAL ----------
cargar_todos_productos()
root.mainloop()
