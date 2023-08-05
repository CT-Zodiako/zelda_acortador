from flask import Blueprint, redirect, url_for, request
from services.add_zelda import guardar_zelda

add_zelda_blueprint = Blueprint('add_zelda', __name__)

@add_zelda_blueprint.route('/add_zelda', methods=['POST'])
def add_zelda():
    zelda = request.form['zelda']
    new_zelda = guardar_zelda(zelda)

    return redirect(url_for('acortar.acortar', id=new_zelda.id))
