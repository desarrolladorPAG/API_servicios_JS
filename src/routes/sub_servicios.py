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
