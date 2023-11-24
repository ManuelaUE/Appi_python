from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors
import os
import uuid
from PIL import Image

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
    
@app.route("/ofertante/register", methods=["POST"])
def registrar_ofertante():
    try:
        tipoDocumento = request.form.get("tipoDocumento")
        numeroDocumento = request.form.get("numeroDocumento")
        fechaNacimiento = request.form.get("fechaNacimiento")
        pais = request.form.get("pais")
        estado = request.form.get("estado")
        ciudad = request.form.get("ciudad")
        direccion = request.form.get("direccion")
        documentoA = request.files["documentoA"]
        documentoB = request.files["documentoB"]
        foto = request.files["foto"]

        public_dir = os.path.join("public")

        if not os.path.exists(public_dir):
            os.makedirs(public_dir)

        nombreDocumentoA = str(uuid.uuid4()) + ".png"
        nombreDocumentoB = str(uuid.uuid4()) + ".png"
        nombreFoto = str(uuid.uuid4()) + ".png"

        rutaDocumentoA = os.path.join(public_dir, nombreDocumentoA)
        rutaDocumentoB = os.path.join(public_dir, nombreDocumentoB)
        rutaFoto = os.path.join(public_dir, nombreFoto)

        documentoA_img = Image.open(documentoA)
        documentoA_img.save(rutaDocumentoA)
        documentoA_img.close()

        documentoB_img = Image.open(documentoB)
        documentoB_img.save(rutaDocumentoB)
        documentoB_img.close()

        foto_img = Image.open(foto)
        foto_img.save(rutaFoto)
        foto_img.close()

        with db.cursor() as cursor:
            sql = "INSERT INTO ofertantes (tipo_documento, numero_documento, fecha_nacimiento, pais, estado, ciudad, direccion, document_a, documento_b, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (tipoDocumento, numeroDocumento, fechaNacimiento, pais, estado, ciudad, direccion, rutaDocumentoA, rutaDocumentoB, rutaFoto))
            db.commit()

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    except FileNotFoundError as e:
        print("Error: Archivo no encontrado -", e)
        return jsonify({"error": "Error: Archivo no encontrado"}), 404
            
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()