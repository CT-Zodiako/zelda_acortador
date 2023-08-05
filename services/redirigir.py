from model import Zeldas, InfoVisitas
from requests import get
from db import db

def obtener_zelda_por_zelda_corto(zelda_corto):
    return Zeldas.query.filter_by(zelda_corto=zelda_corto).first()


def info_por_ip(ip_addr, id_zelda):
    if ip_addr == '127.0.0.1':
        loc = get(f'https://ipapi.co/8.8.8.8/json/')
    else:
        loc = get(f'https://ipapi.co/{ip_addr}/json/')

    country_code = loc.json()['country_code']
    country_name = loc.json()['country_name']

    info_visita = InfoVisitas(ip_user=ip_addr, country_code=country_code, country_name=country_name, id_zelda=id_zelda)
    db.session.add(info_visita)
    db.session.commit()

