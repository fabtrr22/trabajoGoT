from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="admin",
        password="root",
        database="got_fanpage"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temporadas', methods=['GET', 'POST'])
def temporadas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.form['imagen']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO temporadas (nombre, descripcion, imagen) VALUES (%s, %s, %s)',
                       (nombre, descripcion, imagen))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('temporadas'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM temporadas')
    temporadas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('temporadas.html', temporadas=temporadas)

if __name__ == '__main__':
    app.run(debug=True)
