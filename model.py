from db import db

class Zeldas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zelda_original = db.Column(db.String(255), nullable=False)
    zelda_corto = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Zelda {self.id}>'



class InfoVisitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_user = db.Column(db.String(255), nullable=False)
    creacion = db.Column(db.DateTime, server_default=db.func.now())
    country_code = db.Column(db.String, nullable=False)
    country_name = db.Column(db.String, nullable=False)
    id_zelda = db.Column(db.ForeignKey('zeldas.id'), nullable=False)

    def __repr__(self):
        return f'<InfoVisitas {self.id}>'