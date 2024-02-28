from flask import jsonify, request
from models.tipo_asignaciones import *
import uuid
import binascii

def crear_tipo_asignacion():
    try:
        id_tipo_asignacion = uuid.uuid4().bytes
        nombre_asignacion = request.json['nombre_asignacion']

        new_tipo_asignacion = Tipo_asignaciones(id_tipo_asignacion, nombre_asignacion)
        db.session.add(new_tipo_asignacion)
        db.session.commit()

        return jsonify({"message" : "Tipo de asignacion creado correctamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500