from flask import Flask, render_template, request, redirect, url_for, jsonify,render_template, abort
from db import db
from model import Zeldas, InfoVisitas
import hashlib
from requests import get

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Leahtovar2017.@localhost/zeldas_orm'

db.init_app(app)
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_zelda', methods=['POST'])
def add_zelda():
    if request.method == 'POST':
        zelda = request.form['zelda']
        zelda_corto = acortar_url(zelda)

        new_zelda = Zeldas(zelda_original=zelda, zelda_corto=zelda_corto)
        db.session.add(new_zelda)
        db.session.commit()

        return redirect(url_for('acortar', id=new_zelda.id))


@app.route('/acortar/<int:id>', methods=['GET'])
def acortar(id):
    zelda = Zeldas.query.get(id)
    if zelda:
        return render_template('url_acortado.html', zelda=zelda)
    else:
        abort(404)


@app.route("/redirigir/<string:acortado>")
def redirigir(acortado):
    zelda = Zeldas.query.filter_by(zelda_corto=acortado).first()
    if zelda:
        ip_addr = request.remote_addr
        loc = get(f'https://ipapi.co/8.8.8.8/json/')
        country_code = loc.json()['country_code']
        country_name = loc.json()['country_name']
        info_visita = InfoVisitas(ip_user=ip_addr, country_code=country_code, country_name=country_name, id_zelda=zelda.id)
        db.session.add(info_visita)
        db.session.commit()

        return redirect(zelda.zelda_original, code=302)
    else:
        abort(404)



def acortar_url(url):
    
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    short_url = hash_hex[:10]
    
    return short_url

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3001, debug=True)