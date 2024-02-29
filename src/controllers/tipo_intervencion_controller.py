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