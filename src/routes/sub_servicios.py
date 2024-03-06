from flask import Blueprint
from flask_cors import cross_origin
from controllers import sub_servicio_controller
from flask_jwt_extended import jwt_required,get_jwt_identity


sub_servicio = Blueprint('sub_servicio', __name__, url_prefix='/api/v1')

@cross_origin()
@sub_servicio.route("sub_servicio/<id_servicio>", methods = ['POST'])
@jwt_required()
def crear_sub_servicio(id_servicio):
    id_usuario = get_jwt_identity()
    return sub_servicio_controller.crear_sub_servicio(id_servicio, id_usuario)

@cross_origin()
@sub_servicio.route("sub_servicio/<id_sub_servicio>", methods = ['PUT'])
def editar_sub_servicio(id_sub_servicio):
    return sub_servicio_controller.editar_sub_servicio(id_sub_servicio)

@cross_origin()
@sub_servicio.route("sub_servicios", methods = ['GET'])
def obtener_sub_servicios():
    return sub_servicio_controller.obtener_sub_servicios()