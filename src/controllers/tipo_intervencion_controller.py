from flask import jsonify, request
from models.tipo_intervenciones import *
import uuid
import binascii

def crear_tipo_intervencion():
    try:
        id_tipo_intervencion = uuid.uuid4().bytes
        id_tipo_cliente = request.json["id_tipo_cliente"]
        nombre_tipo_intervencion = request.json["nombre_tipo_intervencion"]

        id_tipo_cliente_bytes = binascii.unhexlify(id_tipo_cliente)

        new_tipo_intervencion = Tipo_intervenciones(id_tipo_intervencion, id_tipo_cliente_bytes, nombre_tipo_intervencion)
        db.session.add(new_tipo_intervencion)
        db.session.commit()

        return jsonify({"message" : "Tipo de intervencion creado correctamente", "status" : 200})
    
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

