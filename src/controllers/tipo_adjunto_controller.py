from flask import jsonify, request
from models.tipo_adjuntos import *
import uuid
import binascii

def crear_tipo_adjunto():
    try:
        id_tipo_adjunto = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        nombre_tipo = request.json['nombre_tipo']

        new_tipo_adjunto = Tipo_adjuntos(id_tipo_adjunto, nombre_tipo)
        db.session.add(new_tipo_adjunto)
        db.session.commit()

        return jsonify({"message": "Tipo de adjunto creado correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500