from flask import Blueprint
from flask_cors import cross_origin
from controllers import tipo_intervencion_controller

tipo_intervencion = Blueprint('tipo_intervencion', __name__,url_prefix='/api/v1')

@cross_origin
@tipo_intervencion.route('/tipo_intervencion', methods=['POST'])
def crear_tipo_intervencion():
    return tipo_intervencion_controller.crear_tipo_intervencion()