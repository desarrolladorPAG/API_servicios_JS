from flask import jsonify, request
from models.tipo_clientes import *
import uuid
import binascii

def crear_tipo_cliente():
    try:
        id_tipo_cliente = uuid.uuid4().bytes
        nombre_cliente = request.json['nombre_cliente']

        new_tipo_cliente = Tipo_clientes(id_tipo_cliente, nombre_cliente)
        db.session.add(new_tipo_cliente)
        db.session.commit()

        return jsonify({"message" : "Cliente creado correctamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_tipos_clientes():
    try:
        lista = []
        tipo_clientes = db.session.query(Tipo_clientes).all()

        for tipo_cliente in tipo_clientes:
            datos = {"id_tipo_cliente" : binascii.hexlify(tipo_cliente.id_tipo_cliente).decode(), "nombre_cliente" : tipo_cliente.nombre_cliente}
            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500