from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from decouple import config
from utils.db import db
from routes.roles import roles
from routes.usuarios import usuarios
from routes.tipo_adjuntos import tipo_adjuntos
from routes.estados_servicio import estados_servicio
from routes.tipo_asignacion import tipo_asignacion
from routes.tipo_cliente import tipo_cliente
from routes.tipo_intervenciones import tipo_intervencion
from routes.login import login
from routes.servicio import servicios
from routes.clientes_generales import cliente_general
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:barranquilla91#$%@localhost/servicios_js'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
app.config["JWT_SECRET_KEY"] = config('JWT_SECRET_KEY')

jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(roles)
app.register_blueprint(usuarios)
app.register_blueprint(tipo_adjuntos)
app.register_blueprint(estados_servicio)
app.register_blueprint(tipo_asignacion)
app.register_blueprint(tipo_cliente)
app.register_blueprint(tipo_intervencion)
app.register_blueprint(login)
app.register_blueprint(servicios)
app.register_blueprint(cliente_general)

if __name__=="__main__":
    app.run(port=5000, debug=True)