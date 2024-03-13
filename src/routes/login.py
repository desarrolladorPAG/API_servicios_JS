from flask import Blueprint
from flask_cors import cross_origin
from controllers import login_controller

login = Blueprint('login', __name__,url_prefix='/api/v1')

@cross_origin()
@login.route('/login', methods=['POST'])
def login_normal():
    return login_controller.login()

@cross_origin()
@login.route('/login_google', methods=['POST'])
def login_google():
    return login_controller.login_google()

@cross_origin()
@login.route('/registro', methods=['POST'])
def registro():
    return login_controller.registro()

@cross_origin()
@login.route('/verificar/<token>', methods=['POST'])
def verificar_correo(token):
    return login_controller.verificar_correo(token)