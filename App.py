from flask import Flask
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Leahtovar2017.@localhost/zeldas_orm'
app.secret_key = 'mysecretkey'

db.init_app(app)

# Importar el objeto Blueprint y registrar la ruta en la aplicación
from routes.index import index_blueprint
from routes.add_zelda import add_zelda_blueprint
from routes.acortar import acortar_blueprint
from routes.redirigir import redirigir_blueprint


# Registrar las rutas en la aplicación
app.register_blueprint(index_blueprint)
app.register_blueprint(add_zelda_blueprint)
app.register_blueprint(acortar_blueprint)
app.register_blueprint(redirigir_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3001, debug=True)
