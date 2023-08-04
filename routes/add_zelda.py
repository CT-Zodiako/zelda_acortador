
from flask import Blueprint, render_template, url_for ,redirect,request
from db import db
from model import Zeldas
import hashlib

add_zelda_blueprint = Blueprint('add_zelda', __name__)

@add_zelda_blueprint.route('/add_zelda', methods=['POST'])
def add_zelda():
    if request.method == 'POST':
        zelda = request.form['zelda']
        zelda_corto = acortar_url(zelda)

        new_zelda = Zeldas(zelda_original=zelda, zelda_corto=zelda_corto)
        db.session.add(new_zelda)
        db.session.commit()

        # Cambia el url_for para que haga referencia al endpoint completo 'acortar.acortar'
        return redirect(url_for('acortar.acortar', id=new_zelda.id))

def acortar_url(url):
    
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    short_url = hash_hex[:10]
    
    return short_url