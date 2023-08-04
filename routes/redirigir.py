from flask import Blueprint, redirect, abort, request
from requests import get
from db import db
from model import Zeldas, InfoVisitas

redirigir_blueprint = Blueprint('redirigir', __name__)

@redirigir_blueprint.route("/redirigir/<string:acortado>")
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