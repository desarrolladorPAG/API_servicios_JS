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

def editar_cierre_tecnico(id_cierre_tecnico):
    try:
        id_cierre_tecnico_bytes = binascii.unhexlify(id_cierre_tecnico)

        cierre_tecnico = db.session.query(Cierres_tecnicos).get(id_cierre_tecnico_bytes)

        cierre_tecnico.fecha_cierre = request.json["fecha_cierre"]
        cierre_tecnico.estado_servicio_id = binascii.unhexlify(request.json["estado_servicio_id"]) 
        cierre_tecnico.descripcion = request.json["descripcion"]

        db.session.commit()

        return jsonify({"message" : "Servicio actualizado exitosamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_cierres_tecnicos():
    try:
        lista = []
        cierres_tecnicos = db.session.query(Cierres_tecnicos).all()

        for cierre in cierres_tecnicos:
            if cierre.servicio_id == None:
                servicio_id = None
            else :
                servicio_id = binascii.hexlify(cierre.servicio_id).decode()
            
            if cierre.sub_servicio_id == None:
                sub_servicio_id = None
            else:
                sub_servicio_id = binascii.hexlify(cierre.sub_servicio_id).decode()

            datos = {
                "id_cierre_tecnico" : binascii.hexlify(cierre.id_cierre_tecnico).decode() , 
                "servicio_id" :  servicio_id, 
                "sub_servicio_id" : sub_servicio_id, 
                "fecha_cierre" : cierre.fecha_cierre.strftime('%d/%m/%y'), 
                "estado_servicio_id" : binascii.hexlify(cierre.estado_servicio_id).decode(), 
                "usuario_id" : binascii.hexlify(cierre.usuario_id).decode(), 
                "descripcion" : cierre.descripcion}

            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def eliminar_cierre_tecnico(id_cierre_tecnico):
    try:
        id_cierre_tecnico_bytes = binascii.unhexlify(id_cierre_tecnico)

        cierre_tecnico = db.session.query(Cierres_tecnicos).get(id_cierre_tecnico_bytes)

        if not cierre_tecnico:
            return jsonify({"message" : "Cierre tecnico no encontrado", "status" : 404}) , 404
        
        db.session.delete(cierre_tecnico)
        db.session.commit()

        return jsonify({"message" : "Cierre tecnico eliminado", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

