from flask import jsonify, request
from models.roles import *
import uuid
import binascii

def crear_rol():
    try:
        id_rol = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        nombre_rol = request.json["nombre_rol"]

        new_rol = Roles(id_rol,nombre_rol)
        db.session.add(new_rol)
        db.session.commit()

        return jsonify({"message": "Rol creado correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500


