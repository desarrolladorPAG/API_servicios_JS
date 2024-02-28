from flask import Blueprint
from flask_cors import cross_origin
from controllers import tipo_adjunto_controller

tipo_adjuntos = Blueprint('tipo_adjuntos', __name__, url_prefix='/api/v1')

@cross_origin()
@tipo_adjuntos.route("tipo_adjuntos", methods = ['POST'])
def crear_tipo_adjunto():
    return tipo_adjunto_controller.crear_tipo_adjunto()
