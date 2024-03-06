from flask import jsonify, request
from models.tipo_intervenciones import *
import uuid
import binascii

def crear_tipo_intervencion(id_tipo_cliente_escogido, nuevo_nombre_tipo_intervencion):
    try:
        id_tipo_intervencion = uuid.uuid4().bytes
        id_tipo_cliente = id_tipo_cliente_escogido
        nombre_tipo_intervencion = nuevo_nombre_tipo_intervencion

        new_tipo_intervencion = Tipo_intervenciones(id_tipo_intervencion, id_tipo_cliente, nombre_tipo_intervencion)
        db.session.add(new_tipo_intervencion)
        db.session.commit()

        return id_tipo_intervencion
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_tipo_intervenciones():
    try:
        lista = []
        tipo_intervenciones = db.session.query(Tipo_intervenciones).all()

        for tipo in tipo_intervenciones:
            datos = {"id_tipo_intervencion": binascii.hexlify(tipo.id_tipo_intervencion).decode(), "tipo_cliente_id" : binascii.hexlify(tipo.tipo_cliente_id).decode(), "nombre" : tipo.nombre_tipo_intervencion}

            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

