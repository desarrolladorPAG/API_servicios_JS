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

@cross_origin()
@cierre_tecnico.route('/cierre_tecnico/<id_cierre_tecnico>', methods=['PUT'])
def editar_cierre_tecnico(id_cierre_tecnico):
    return cierre_tecnico_controller.editar_cierre_tecnico(id_cierre_tecnico)

@cross_origin()
@cierre_tecnico.route('/cierres_tecnicos', methods=['GET'])
def obtener_cierres_tecnicos():
    return cierre_tecnico_controller.obtener_cierres_tecnicos()

@cross_origin()
@cierre_tecnico.route('/cierre_tecnico/<id_cierre_tecnico>', methods=['DELETE'])
def eliminar_cierre_tecnico(id_cierre_tecnico):
    return cierre_tecnico_controller.eliminar_cierre_tecnico(id_cierre_tecnico)