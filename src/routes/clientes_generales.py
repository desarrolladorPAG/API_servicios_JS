from flask import Blueprint
from flask_cors import cross_origin
from controllers import cliente_general_controller

cliente_general = Blueprint('cliente_general', __name__,url_prefix='/api/v1')

@cross_origin()
@cliente_general.route('/clientes_generales', methods=['GET'])
def obtener_clientes_generales():
    return cliente_general_controller.obtener_clientes_generales()
