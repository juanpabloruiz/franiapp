from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_stock(codigo):
    conn = sqlite3.connect('productos.db')
    cur = conn.cursor()
    cur.execute("SELECT nombre, stock FROM productos WHERE codigo_barra = ?", (codigo,))
    row = cur.fetchone()
    conn.close()
    return row

@app.route('/api/stock', methods=['GET'])
def stock():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({'error': 'Falta código'}), 400

    resultado = get_stock(codigo)
    if resultado:
        nombre, stock = resultado
        return jsonify({'nombre': nombre, 'stock': stock})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
