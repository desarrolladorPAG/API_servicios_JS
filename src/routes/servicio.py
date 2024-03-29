from flask import Blueprint
from flask_cors import cross_origin
from controllers import servicio_controller
from flask_jwt_extended import jwt_required,get_jwt_identity

servicios = Blueprint('servicios', __name__,url_prefix='/api/v1')

@cross_origin()
@servicios.route('/servicio', methods=['POST'])
@jwt_required()
def crear_servicio():
    id_usuario = get_jwt_identity()
    return servicio_controller.crear_servicio(id_usuario)

@cross_origin()
@servicios.route('/servicios', methods=['GET'])
def obtener_servicios():
    return servicio_controller.obtener_servicios()

@cross_origin()
@servicios.route('/servicio/<id_servicio>', methods=['PUT'])
def editar_servicio(id_servicio):
    return servicio_controller.editar_servicio(id_servicio)

@cross_origin()
@servicios.route('/servicio/<id_servicio>', methods=['DELETE'])
def eliminar_servicio(id_servicio):
    return servicio_controller.eliminar_servicio(id_servicio)