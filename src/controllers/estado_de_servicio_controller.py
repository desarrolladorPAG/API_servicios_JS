from flask import jsonify, request
from models.estados_de_servicio import *
import uuid
import binascii

def crear_estado_de_servicio():
    try:
        id_estado_servicio = uuid.uuid4().bytes
        nombre_estado = request.json['nombre_estado']

        new_estado_servicio = Estados_de_servicio(id_estado_servicio, nombre_estado)
        db.session.add(new_estado_servicio)
        db.session.commit()

        return jsonify({"message" : "Estado de servicio creado correctamente" , "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_estados_de_servicio():
    try:
        lista = []
        estados_de_servicio = db.session.query(Estados_de_servicio).all()

        for estado in estados_de_servicio:
            datos = {"id_estado_servicio" : binascii.hexlify(estado.id_estado_servicio).decode() , "nombre" : estado.nombre_estado}
            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500