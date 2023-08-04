from flask import Blueprint, render_template, abort
from model import Zeldas

acortar_blueprint = Blueprint('acortar', __name__)

@acortar_blueprint.route('/acortar/<int:id>', methods=['GET'])
def acortar(id):
    zelda = Zeldas.query.get(id)
    if zelda:
        return render_template('url_acortado.html', zelda=zelda)
    else:
        abort(404)