from flask import Blueprint
from flask_cors import cross_origin
from controllers import tipo_cliente_controller

tipo_cliente = Blueprint("tipo_cliente", __name__, url_prefix='/api/v1')

@cross_origin()
@tipo_cliente.route("tipo_cliente", methods = ['POST'])
def crear_tipo_cliente():
    return tipo_cliente_controller.crear_tipo_cliente()

@cross_origin()
@tipo_cliente.route("tipo_cliente", methods = ['GET'])
def obtener_tipo_clientes():
    return tipo_cliente_controller.obtener_tipos_clientes()