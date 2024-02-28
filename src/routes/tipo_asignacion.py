from flask import Blueprint
from flask_cors import cross_origin
from controllers import tipo_asignacion_controller

tipo_asignacion = Blueprint('tipo_asignacion', __name__, url_prefix='/api/v1')

@cross_origin()
@tipo_asignacion.route("tipo_asignacion", methods = ['POST'])
def crear_tipo_asignacion():
    return tipo_asignacion_controller.crear_tipo_asignacion()