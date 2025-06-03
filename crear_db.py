import sqlite3

conn = sqlite3.connect('productos.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barra TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
)
''')

# Producto de prueba
c.execute("INSERT OR IGNORE INTO productos (codigo_barra, nombre, stock) VALUES (?, ?, ?)",
          ("1234567890123", "Coca-Cola 1.5L", 15))

conn.commit()
conn.close()
print("Base de datos creada.")
