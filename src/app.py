from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from decouple import config

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:barranquilla91#$%@localhost/servicios_js'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
app.config["JWT_SECRET_KEY"] = config('JWT_SECRET_KEY')

jwt = JWTManager(app)

if __name__=="__main__":
    app.run(port=5000, debug=True)