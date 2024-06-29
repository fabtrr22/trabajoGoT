from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/temporadas.html')
def temporadas():
    return render_template('temporadas.html')

@app.route('/personajes.html')
def personajes():
    return render_template('personajes.html')

@app.route('/contacto.html')
def contacto():
    return render_template('contacto.html')

class Temporadas:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS temporadas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero INT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255),
            imagen_url VARCHAR(255)
        )''')
        self.conn.commit()

    def agregar_temporada(self, numero, titulo, descripcion, imagen_url):
        sql = "INSERT INTO temporadas (numero, titulo, descripcion, imagen_url) VALUES (%s, %s, %s, %s)"
        valores = (numero, titulo, descripcion, imagen_url)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def consultar_temporada(self, id):
        self.cursor.execute("SELECT * FROM temporadas WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def modificar_temporada(self, id, numero, titulo, descripcion, imagen_url):
        sql = "UPDATE temporadas SET numero = %s, titulo = %s, descripcion = %s, imagen_url = %s WHERE id = %s"
        valores = (numero, titulo, descripcion, imagen_url, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def listar_temporadas(self):
        self.cursor.execute("SELECT * FROM temporadas")
        return self.cursor.fetchall()

    def eliminar_temporada(self, id):
        self.cursor.execute("DELETE FROM temporadas WHERE id = %s", (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

# creo instancia de la clase Temporadas
temporadas = Temporadas(host='localhost', user='root', password='root', database='got')


#------------ Personaje--------------------
class Personajes:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS personajes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255),
            imagen_url VARCHAR(255)
        )''')
        self.conn.commit()

    def agregar_personaje(self, nombre, descripcion, imagen_url):
        sql = "INSERT INTO personajes (nombre, descripcion, imagen_url) VALUES (%s, %s, %s)"
        valores = (nombre, descripcion, imagen_url)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def consultar_personaje(self, id):
        self.cursor.execute("SELECT * FROM personajes WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def modificar_personaje(self, id, nombre, descripcion, imagen_url):
        sql = "UPDATE personajes SET nombre = %s, descripcion = %s, imagen_url = %s WHERE id = %s"
        valores = (nombre, descripcion, imagen_url, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def listar_personajes(self):
        self.cursor.execute("SELECT * FROM personajes")
        return self.cursor.fetchall()

    def eliminar_personaje(self, id):
        self.cursor.execute("DELETE FROM personajes WHERE id = %s", (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

# creo instancia de la clase Personajes
personajes = Personajes(host='localhost', user='root', password='root', database='got')
#--------------------------------

# aqui se guardan las imagenes
ruta_destino = './static/img/'

@app.route("/temporadas", methods=["GET"])
def listar_temporadas():
    listado = temporadas.listar_temporadas()
    return jsonify(listado)

@app.route("/temporadas/<int:id>", methods=["GET"])
def mostrar_temporada(id):
    temporada = temporadas.consultar_temporada(id)
    if temporada:
        return jsonify(temporada), 200
    else:
        return "Temporada no encontrada", 404

@app.route("/temporadas", methods=["POST"])
def agregar_temporada():
    try:
        numero = request.form['numero']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        nombre_imagen = ""

        if imagen:
            nombre_imagen = secure_filename(imagen.filename)
            nombre_base, extension = os.path.splitext(nombre_imagen)
            nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
            imagen.save(os.path.join(ruta_destino, nombre_imagen))

        nueva_temporada_id = temporadas.agregar_temporada(numero, titulo, descripcion, nombre_imagen)
        if nueva_temporada_id:
            return jsonify({"mensaje": "Temporada agregada correctamente.", "id": nueva_temporada_id, "imagen": nombre_imagen}), 201
        else:
            return jsonify({"mensaje": "Error al agregar la temporada."}), 500
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500

@app.route("/temporadas/<int:id>", methods=["PUT"])
def modificar_temporada(id):
    numero = request.form.get("numero")
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    imagen = request.files.get('imagen')
    nombre_imagen = ""

    if imagen:
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
        temporada = temporadas.consultar_temporada(id)
        if temporada and temporada["imagen_url"]:
            ruta_imagen = os.path.join(ruta_destino, temporada["imagen_url"])
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:
        temporada = temporadas.consultar_temporada(id)
        if temporada:
            nombre_imagen = temporada["imagen_url"]

    if temporadas.modificar_temporada(id, numero, titulo, descripcion, nombre_imagen):
        return jsonify({"mensaje": "Temporada modificada"}), 200
    else:
        return jsonify({"mensaje": "Temporada no encontrada"}), 404

@app.route("/temporadas/<int:id>", methods=["DELETE"])
def eliminar_temporada(id):
    temporada = temporadas.consultar_temporada(id)
    if temporada:
        if temporada["imagen_url"]:
            ruta_imagen = os.path.join(ruta_destino, temporada["imagen_url"])
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
        if temporadas.eliminar_temporada(id):
            return jsonify({"mensaje": "Temporada eliminada"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar la temporada"}), 500
    else:
        return jsonify({"mensaje": "Temporada no encontrada"}), 404

#--------@app route Personajes-----------------------
@app.route("/personajes", methods=["GET"])
def listar_personajes():
    listado = personajes.listar_personajes()
    return jsonify(listado)

@app.route("/personajes/<int:id>", methods=["GET"])
def mostrar_personaje(id):
    personaje = personajes.consultar_personaje(id)
    if personaje:
        return jsonify(personaje), 200
    else:
        return "Personaje no encontrado", 404

@app.route("/personajes", methods=["POST"])
def agregar_personaje():
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        nombre_imagen = ""

        if imagen:
            nombre_imagen = secure_filename(imagen.filename)
            nombre_base, extension = os.path.splitext(nombre_imagen)
            nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
            imagen.save(os.path.join(ruta_destino, nombre_imagen))

        nuevo_personaje_id = personajes.agregar_personaje(nombre, descripcion, nombre_imagen)
        if nuevo_personaje_id:
            return jsonify({"mensaje": "Personaje agregado correctamente.", "id": nuevo_personaje_id, "imagen": nombre_imagen}), 201
        else:
            return jsonify({"mensaje": "Error al agregar el personaje."}), 500
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500

@app.route("/personajes/<int:id>", methods=["PUT"])
def modificar_personaje(id):
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    imagen = request.files.get('imagen')
    nombre_imagen = ""

    if imagen:
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
        personaje = personajes.consultar_personaje(id)
        if personaje and personaje["imagen_url"]:
            ruta_imagen = os.path.join(ruta_destino, personaje["imagen_url"])
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:
        personaje = personajes.consultar_personaje(id)
        if personaje:
            nombre_imagen = personaje["imagen_url"]

    if personajes.modificar_personaje(id, nombre, descripcion, nombre_imagen):
        return jsonify({"mensaje": "Personaje modificado"}), 200
    else:
        return jsonify({"mensaje": "Personaje no encontrado"}), 404

@app.route("/personajes/<int:id>", methods=["DELETE"])
def eliminar_personaje(id):
    personaje = personajes.consultar_personaje(id)
    if personaje:
        if personaje["imagen_url"]:
            ruta_imagen = os.path.join(ruta_destino, personaje["imagen_url"])
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
        if personajes.eliminar_personaje(id):
            return jsonify({"mensaje": "Personaje eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el personaje"}), 500
    else:
        return jsonify({"mensaje": "Personaje no encontrado"}), 404

#----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
