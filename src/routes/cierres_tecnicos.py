from flask import Blueprint
from flask_cors import cross_origin
from controllers import cierre_tecnico_controller
from flask_jwt_extended import jwt_required,get_jwt_identity

cierre_tecnico = Blueprint('cierre_tecnico', __name__,url_prefix='/api/v1')

@cross_origin()
@cierre_tecnico.route('/cierre_tecnico', methods=['POST'])
@jwt_required()
def obtener_clientes_generales():
    id_usuario = get_jwt_identity()
    return cierre_tecnico_controller.crear_cierre_tecnico(id_usuario)
