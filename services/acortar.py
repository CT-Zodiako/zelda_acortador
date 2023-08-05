from model import Zeldas

def obtener_zelda_por_id(id):
    return Zeldas.query.get(id)
