from flask import Blueprint
from flask_cors import cross_origin
from controllers import numeros_contables_controller
from flask_jwt_extended import jwt_required,get_jwt_identity

numero_contable = Blueprint('numero_contable', __name__,url_prefix='/api/v1')

@cross_origin()
@numero_contable.route('/numero_contable', methods=['POST'])
@jwt_required()
def crear_numero_contable():
    id_usuario = get_jwt_identity()
    return numeros_contables_controller.crear_numero_contable(id_usuario)

@cross_origin()
@numero_contable.route('/numero_contable/<id_numero_contable>', methods=['PUT'])
def editar_numero_contable(id_numero_contable):
    return numeros_contables_controller.editar_numero_contable(id_numero_contable)

@cross_origin()
@numero_contable.route('/numeros_contables', methods=['GET'])
def obtener_numeros_contable():
    return numeros_contables_controller.obtener_numeros_contables()
