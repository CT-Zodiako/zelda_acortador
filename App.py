from flask import Flask, render_template, request ,redirect, url_for
import psycopg2
import hashlib


app = Flask(__name__)

try:
    conn = psycopg2.connect(
        host="localhost",
        user='postgres',
        password='Leahtovar2017.',
        database='acortador_zeldas'
        )
    print("Conexión exitosa")
except psycopg2.Error as e:
    print("Error en la conexión: {e}")


app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_zelda', methods=['POST'])
def add_zelda():
    if request.method == 'POST':
        zelda = request.form['zelda']
        zelda_corto = acortar_url(zelda)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO zeldas (zelda_original, zelda_corto) VALUES (%s, %s)', (zelda,zelda_corto))
        conn.commit()
        cursor.execute('SELECT id FROM zeldas WHERE zelda_original = %s', (zelda,))
        data = cursor.fetchall()
        id = data[0][0]

        return redirect(url_for('acortar', id = id))
        


@app.route('/acortar/<id>', methods=['GET'])
def acortar(id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM zeldas WHERE id = {0}'.format(id))
    data = cursor.fetchall()
    return render_template('url_acortado.html', zelda = data[0], )


@app.route("/<string:acortado>")
def redirigir(acortado):

    cursor = conn.cursor()
    cursor.execute('SELECT zelda_original FROM zeldas WHERE zelda_corto = %s', (acortado,))
    data = cursor.fetchall()
    url_original = data[0][0]
    print(url_original)
    if url_original:
        # Si encontramos la URL original, redirigimos al usuario a ella
        return redirect(url_original, code=302)
    else:
        # Si la URL acortada no existe, se puede mostrar un mensaje de error o redirigir a una página 404
        return "URL acortada no encontrada", 404




def acortar_url(url):
    
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    
    short_url = hash_hex[:10]
    
    return short_url

if __name__ == '__main__':
    app.run(port = 3001 , debug = True)