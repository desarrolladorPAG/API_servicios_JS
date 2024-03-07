from flask import jsonify, request
from models.archivos_adjuntos import *
import uuid
import binascii
from sqlalchemy.exc import IntegrityError

def adjuntar_archivo(id_usuario):
    try:
        id_archivo_adjunto = uuid.uuid4().bytes
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
        
        tipo_adjunto_id = binascii.unhexlify(request.json["tipo_adjunto_id"])
        usuario_id = binascii.unhexlify(id_usuario)
        ruta_archivo = request.json["ruta_archivo"]

        new_archivo_adjunto = Archivos_adjuntos(id_archivo_adjunto, servicio_id, sub_servicio_id, tipo_adjunto_id, usuario_id, ruta_archivo)
        db.session.add(new_archivo_adjunto)
        db.session.commit()

        return jsonify({"message" : "Archivo adjunto correctamente" , "status" : 200})
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_archivos_adjuntos():
    try:
        lista = []
        archivos_adjuntos = db.session.query(Archivos_adjuntos).all()

        for archivo_adjunto in archivos_adjuntos:
            if archivo_adjunto.servicio_id == None:
                servicio_id = None
            else :
                servicio_id = binascii.hexlify(archivo_adjunto.servicio_id).decode()
            
            if archivo_adjunto.sub_servicio_id == None:
                sub_servicio_id = None
            else:
                sub_servicio_id = binascii.hexlify(archivo_adjunto.sub_servicio_id).decode()

            datos = {"id_archivo_adjunto" : binascii.hexlify(archivo_adjunto.id_archivo_adjunto).decode(), "servicio_id" : servicio_id, "sub_servicio_id" : sub_servicio_id, "tipo_adjunto_id" : binascii.hexlify(archivo_adjunto.tipo_adjunto_id).decode(), "usuario_id" : binascii.hexlify(archivo_adjunto.usuario_id).decode(), "ruta_archivo" : archivo_adjunto.ruta_archivo}

            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500
    
def eliminar_archivo_adjunto(id_archivo_adjunto):
    try:
        id_archivo_adjunto_bytes = binascii.unhexlify(id_archivo_adjunto)

        archivo_adjunto = db.session.query(Archivos_adjuntos).get(id_archivo_adjunto_bytes)

        if not archivo_adjunto:
            return jsonify({"message" : "Archivo adjunto no encontrado", "status" : 404}) , 404

        db.session.delete(archivo_adjunto)
        db.session.commit()

        return jsonify({"message" : "Archivo adjunto eliminado", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

