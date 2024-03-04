from flask import jsonify, request
from models.servicios import *
from controllers import cliente_general_controller
import uuid
import binascii
from sqlalchemy.exc import IntegrityError
from decouple import config

def crear_servicio(id_usuario_administrativo):
    try:
        id_servicio = uuid.uuid4().bytes
        id_usuario_administrativo_bytes = binascii.unhexlify(id_usuario_administrativo)
        tecnico_usuario_id_bytes = binascii.unhexlify(request.json["tecnico_usuario_id"])
        tipo_intervencion_id_bytes = binascii.unhexlify(request.json["tipo_intervencion_id"])

        numero_servicio = generar_numero_servicio()
        fecha_solicitud = request.json["fecha_solicitud"]
        tipo_cliente_id = request.json["tipo_cliente_id"]
        cliente_general_id = request.json["cliente_general_id"]
        nombre_solicitante = request.json["nombre_solicitante"]
        tipo_de_equipo = request.json["tipo_de_equipo"]
        descripcion = request.json["descripcion"]
        id_activo = request.json["id_activo"]
        
        

        if tipo_cliente_id == config('ID_CLIENTE_GENERAL'):
            if cliente_general_id == None: #Si no se selecciono un cliente general es porque creará uno
                nombre_cliente_general = request.json["nombre_cliente_general"]
                cliente_general_id_bytes = cliente_general_controller.crear_cliente_general(nombre_cliente_general)
            else: #Si la variable cliente_general_id es diferente de nulo es porque escogio un cliente general ya crado
                cliente_general_id_bytes = binascii.unhexlify(cliente_general_id)
        else: #Si no es tipo de cliente general no se guardara un cliente general
            cliente_general_id_bytes = None        
        
        
        tipo_cliente_id_bytes = binascii.unhexlify(tipo_cliente_id)

        new_servicio = Servicios(id_servicio, numero_servicio, fecha_solicitud, tipo_cliente_id_bytes, cliente_general_id_bytes, nombre_solicitante, tipo_de_equipo, descripcion, tecnico_usuario_id_bytes, id_usuario_administrativo_bytes, id_activo, tipo_intervencion_id_bytes)

        db.session.add(new_servicio)
        db.session.commit()

        return jsonify({"message" : "Servicio creado correctamente" , "status" : 200})
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500


def generar_numero_servicio():
    # Consultar el último número de servicio creado
    ultimo_servicio = db.session.query(Servicios).order_by(Servicios.numero_servicio.desc()).first()
    if ultimo_servicio:
        # Obtener el número de servicio del último servicio y convertirlo a entero
        ultimo_numero_servicio = int(ultimo_servicio.numero_servicio.split('-')[0])
        # Incrementar el número de servicio
        nuevo_numero_servicio = ultimo_numero_servicio + 1
    else:
        # Si no hay ningún servicio en la base de datos, comenzar desde 10000
        nuevo_numero_servicio = 10000

    # Formatear el nuevo número de servicio con el sufijo "-00"
    numero_servicio_formateado = f"{nuevo_numero_servicio}-00"
    

    # return numero_servicio_formateado
    return numero_servicio_formateado

