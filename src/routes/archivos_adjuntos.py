from flask import Blueprint
from flask_cors import cross_origin
from controllers import archivos_adjuntos_controller
from flask_jwt_extended import jwt_required,get_jwt_identity

archivo_adjunto = Blueprint('archivo_adjunto', __name__,url_prefix='/api/v1')

@cross_origin()
@archivo_adjunto.route('/archivo_adjunto', methods=['POST'])
@jwt_required()
def adjuntar_archivo():
    id_usuario = get_jwt_identity()
    return archivos_adjuntos_controller.adjuntar_archivo(id_usuario)