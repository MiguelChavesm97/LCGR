from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = 'registros.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        ''')

@app.route('/api/registro', methods=['POST'])
def agregar_registro():
    data = request.json
    nombre = data['nombre']
    fecha = data['fecha']
    hora = data['hora']

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('INSERT INTO registros (nombre, fecha, hora) VALUES (?, ?, ?)', (nombre, fecha, hora))
    
    return jsonify({"mensaje": "Registro guardado"}), 201

@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT nombre, fecha, hora FROM registros')
        registros = [{"nombre": n, "fecha": f, "hora": h} for n, f, h in cursor.fetchall()]
    return jsonify(registros)

@app.route('/api/registros', methods=['DELETE'])
def borrar_registros():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM registros')
    return jsonify({"mensaje": "Todos los registros han sido borrados"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

