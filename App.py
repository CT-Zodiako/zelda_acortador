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
        print(zelda_corto)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO zeldas (zelda_original, zelda_corto) VALUES (%s, %s)', (zelda,zelda_corto))

        conn.commit()


        return redirect(url_for('index'))




def acortar_url(url):
    
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    
    short_url = hash_hex[:10]
    
    return short_url

if __name__ == '__main__':
    app.run(port = 3001 , debug = True)