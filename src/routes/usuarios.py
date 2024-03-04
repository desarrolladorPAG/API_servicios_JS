from flask import Blueprint
from flask_cors import cross_origin
from controllers import usuario_controller

usuarios = Blueprint('usuarios', __name__,url_prefix='/api/v1')

@cross_origin
@usuarios.route('/usuarios', methods=['POST'])
def crear_usuario():
    return usuario_controller.crear_usuario()

@cross_origin
@usuarios.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return usuario_controller.obtener_usuarios()