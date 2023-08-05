from flask import Blueprint, redirect, abort, request
from services.redirigir import obtener_zelda_por_zelda_corto, info_por_ip


redirigir_blueprint = Blueprint('redirigir', __name__)

@redirigir_blueprint.route("/redirigir/<string:acortado>")
def redirigir(acortado):
    zelda = obtener_zelda_por_zelda_corto(acortado)
    if zelda:
        info_por_ip(request.remote_addr, zelda.id)
        return redirect(zelda.zelda_original, code=302)
    else:
        abort(404)