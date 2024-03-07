from flask import jsonify, request
from models.numeros_contables import *
import uuid
import binascii
from sqlalchemy.exc import IntegrityError

def crear_numero_contable(id_usuario):
    try:
        id_numero_contable = uuid.uuid4().bytes
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
        
        tipo_asignacion_id = binascii.unhexlify(request.json["tipo_asignacion_id"])
        usuario_id = binascii.unhexlify(id_usuario)
        numero_documento = request.json["numero_documento"]
        fecha_emision = request.json["fecha_emision"]
        ruta_archivo = request.json["ruta_archivo"]
        observacion = request.json["observacion"]

        new_numero_contable = Numeros_contables(id_numero_contable, servicio_id, sub_servicio_id, tipo_asignacion_id, usuario_id, numero_documento, fecha_emision, ruta_archivo, observacion)

        db.session.add(new_numero_contable)
        db.session.commit()

        return jsonify({"message" : "Numero contable creado correctamente" , "status" : 200})
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500
    
def obtener_numeros_contables():
    try:
        lista = []
        numeros_contables = db.session.query(Numeros_contables).all()

        for numero_contable in numeros_contables:
            if numero_contable.servicio_id == None:
                servicio_id = None
            else :
                servicio_id = binascii.hexlify(numero_contable.servicio_id).decode()
            
            if numero_contable.sub_servicio_id == None:
                sub_servicio_id = None
            else:
                sub_servicio_id = binascii.hexlify(numero_contable.sub_servicio_id).decode()

            datos = {"id_numero_contable" : binascii.hexlify(numero_contable.id_numero_contable).decode(), "servicio_id" : servicio_id, "sub_servicio_id" : sub_servicio_id, "tipo_asignacion_id" : binascii.hexlify(numero_contable.tipo_asignacion_id).decode(), "usuario_id" : binascii.hexlify(numero_contable.usuario_id).decode(), "numero_documento" : numero_contable.numero_documento, "fecha_emision" : numero_contable.fecha_emision, "ruta_archivo" : numero_contable.ruta_archivo, "observacion" : numero_contable.observacion}

            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def editar_numero_contable(id_numero_contable):
    try:
        id_numero_contable_bytes = binascii.unhexlify(id_numero_contable)

        numero_contable = db.session.query(Numeros_contables).get(id_numero_contable_bytes)

        if not numero_contable:
            return jsonify({"message" : "Numero contable no encontrado", "status" : 404}) , 404
        
        numero_contable.tipo_asignacion_id = binascii.unhexlify(request.json["tipo_asignacion_id"])
        numero_contable.numero_documento = request.json["numero_documento"]
        numero_contable.fecha_emision = request.json["fecha_emision"]
        numero_contable.observacion = request.json["observacion"]
        numero_contable.ruta_archivo = request.json["ruta_archivo"]

        db.session.commit()

        return jsonify({"message" : "Numero contable actualizado exitosamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 50

