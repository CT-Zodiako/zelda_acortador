from flask import Flask, render_template, request ,redirect, url_for
import psycopg2
import hashlib
from flask import jsonify

from requests import get

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
    cursor.execute('SELECT * FROM zeldas WHERE id = %s', (id,))
    data = cursor.fetchall()
    return render_template('url_acortado.html', zelda = data[0], )


@app.route("/redirigir/<string:acortado>")
def redirigir(acortado):
    cursor = conn.cursor()
    cursor.execute('SELECT zelda_original, id FROM zeldas WHERE zelda_corto = %s', (acortado,))
    data = cursor.fetchall()
    url_original = data[0][0]
    id_zelda = data[0][1]
    print(data)
    if url_original:

        ip_addr = request.remote_addr
        
        loc = get(f'https://ipapi.co/{ip_addr}/json/')

        country_code = loc.json()['country_code']
        country_name = loc.json()['country_name']
        cursor = conn.cursor()
        cursor.execute('INSERT INTO info_visitas (ip_user, country_code, country_name, id_zelda) VALUES (%s, %s, %s, %s, %s)', (ip_addr,country_code,country_name,id_zelda))
        conn.commit()


        
        
        return redirect(url_original, code=302)
    else:
        # Si la URL acortada no existe, se puede mostrar un mensaje de error o redirigir a una página 404
        return "URL acortada no encontrada", 404


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200



def acortar_url(url):
    
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    short_url = hash_hex[:10]
    
    return short_url

if __name__ == '__main__':
    app.run(port = 3001 , debug = True)