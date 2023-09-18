from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors

app = Flask(__name__)
CORS(app)

# Configura la conexión a MySQL
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='servixdb',
    cursorclass=pymysql.cursors.DictCursor
)

# Ruta para obtener todos los solicitantes
@app.route('/solicitantes', methods=['GET'])
def obtener_solicitantes():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM solicitantes")
        solicitantes = cursor.fetchall()
    return jsonify(solicitantes), 200

# Ruta para crear un nuevo solicitante
@app.route('/solicitante', methods=['POST'])
def crear_solicitante():
    try:
        # Convertimos los datos recibidos en un arreglo para mejor manejo de datos
        
        data = request.json
        
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        telefono = data.get('telefono')
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        
        query = f"INSERT INTO solicitantes (nombre, apellido, telefono, correo, contrasena) VALUES ('{nombre}', '{apellido}', {telefono}, '{correo}', '{contrasena}')"
   
        with db.cursor() as cursor:
            cursor.execute(query)
            db.commit()
        # Devolvemos un arreglo con un mensaje
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    except Exception as e:
        print(e.message)
        # Devolvemos el error producido
        return jsonify({"error": str(e)}), 500

# Ruta para loguear un usuario
@app.route('/solicitante/login', methods=['POST'])
def ingresar_solicitante():
    try:
        data = request.json
        
        contrasena = data.get('contrasena')
        correo = data.get('correo')
        
        query = f"SELECT * FROM solicitantes WHERE correo = '{correo}' AND contrasena = '{contrasena}'"

        with db.cursor() as cursor:
            cursor.execute(query)
            usuarios = cursor.fetchone()
            
            if usuarios is not None:
                return jsonify(usuarios), 200
            else: 
                return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()