import hashlib
from db import db
from model import Zeldas

def acortar_url(url):
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    short_url = hash_hex[:10]
    return short_url

def guardar_zelda(zelda):
    zelda_corto = acortar_url(zelda)

    new_zelda = Zeldas(zelda_original=zelda, zelda_corto=zelda_corto)
    db.session.add(new_zelda)
    db.session.commit()

    return new_zelda
