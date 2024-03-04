from flask import jsonify, request
from models.clientes_generales import *
import uuid
import binascii

def crear_cliente_general(nombre_cliente_general):
    try:
        id_cliente_general = uuid.uuid4().bytes
        
        new_cliente_general = Clientes_generales(id_cliente_general, nombre_cliente_general)
        db.session.add(new_cliente_general)
        db.session.commit()

        return id_cliente_general
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_clientes_generales():
    try:
        lista = []
        clientes_generales = db.session.query(Clientes_generales).all()

        for cliente_general in clientes_generales:
            datos = {"id_cliente_general" : binascii.hexlify(cliente_general.id_cliente_general).decode(), "nombre" : cliente_general.nombre_cliente_general}
            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

