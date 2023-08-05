from flask import Blueprint, render_template, abort
from services.acortar import obtener_zelda_por_id

acortar_blueprint = Blueprint('acortar', __name__)

@acortar_blueprint.route('/acortar/<int:id>', methods=['GET'])
def acortar(id):
    zelda = obtener_zelda_por_id(id)
    if zelda:
        return render_template('url_acortado.html', zelda=zelda)
    else:
        abort(404)
