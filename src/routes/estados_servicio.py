from flask import Blueprint
from flask_cors import cross_origin
from controllers import estado_de_servicio_controller

estados_servicio = Blueprint('estados_servicio', __name__,url_prefix='/api/v1')

@cross_origin()
@estados_servicio.route("estados_servicio", methods=['POST'])
def crear_estado_de_servicio():
    return estado_de_servicio_controller.crear_estado_de_servicio()