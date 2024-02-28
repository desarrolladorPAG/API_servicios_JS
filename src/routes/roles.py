from flask import Blueprint
from flask_cors import cross_origin
from controllers import rol_controller

roles = Blueprint('roles', __name__,url_prefix='/api/v1')

@cross_origin()
@roles.route('/roles', methods=['POST'])
def crear_rol():
    return rol_controller.crear_rol()

@cross_origin()
@roles.route('/roles', methods=['GET'])
def obtener_roles():
    return rol_controller.obtener_roles()