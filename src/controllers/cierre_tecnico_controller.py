from flask import jsonify, request
from models.cierres_tecnicos import *
import uuid
import binascii
from sqlalchemy.exc import IntegrityError


def crear_cierre_tecnico(id_usuario):
    try:
        id_cierre_tecnico = uuid.uuid4().bytes
        servicio_id = request.json["servicio_id"]
        sub_servicio_id = request.json["sub_servicio_id"]

        if servicio_id == None:
            servicio_id = None
        else:
            servicio_id = binascii.unhexlify(request.json["servicio_id"])
        
        if sub_servicio_id == None:
            sub_servicio_id = None
        else:
            sub_servicio_id = binascii.unhexlify(request.json["sub_servicio_id"])
        
        usuario_id = binascii.unhexlify(id_usuario) 
        estado_servicio_id = binascii.unhexlify(request.json["estado_servicio_id"])
        fecha_cierre = request.json["fecha_cierre"]
        descripcion = request.json["descripcion"]

        new_cierre_tecnico = Cierres_tecnicos(id_cierre_tecnico, servicio_id, sub_servicio_id, fecha_cierre, estado_servicio_id, usuario_id, descripcion)


        db.session.add(new_cierre_tecnico)
        db.session.commit()

        return jsonify({"message" : "Cierre tecnico creado correctamente" , "status" : 200})
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500
        






