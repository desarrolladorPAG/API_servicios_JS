from flask import jsonify, request
from models.sub_servicios import *
from models.servicios import Servicios
import uuid
import binascii
from sqlalchemy.exc import IntegrityError
from controllers import tipo_intervencion_controller

def crear_sub_servicio(id_servicio, id_usuario_administrativo):
    try:
        id_sub_servicio = uuid.uuid4().bytes
        servicio_id_bytes = binascii.unhexlify(id_servicio)
        administrativo_usuario_id_bytes = binascii.unhexlify(id_usuario_administrativo)
        tecnico_usuario_id = binascii.unhexlify(request.json["tecnico_usuario_id"])
        tipo_cliente_id = binascii.unhexlify(request.json["tipo_cliente_id"])

        numero_sub_servicio = generar_numero_subservicio(servicio_id_bytes)

        fecha_solicitud = request.json["fecha_solicitud"]
        nombre_solicitante = request.json["nombre_solicitante"]
        descripcion = request.json["descripcion"]


        if request.json["nuevo_tipo_intervencion"] != None: #Si se manda un nuevo nombre de tipo de intervencio, se debe crear en la base de datos
            tipo_intervencion_id = tipo_intervencion_controller.crear_tipo_intervencion(tipo_cliente_id, request.json["nuevo_tipo_intervencion"] )
        else:
            tipo_intervencion_id = binascii.unhexlify(request.json["tipo_intervencion_id"])

        new_sub_servicio = Sub_servicios(id_sub_servicio,servicio_id_bytes, tipo_cliente_id, tipo_intervencion_id, tecnico_usuario_id,administrativo_usuario_id_bytes, numero_sub_servicio, fecha_solicitud, nombre_solicitante, descripcion)

        db.session.add(new_sub_servicio)
        db.session.commit()

        return jsonify({"message" : "Sub-servicio creado correctamente" , "status" : 200})

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500



def generar_numero_subservicio(id_servicio_bytes):

    servicio = Servicios.query.get(id_servicio_bytes)
    if not servicio:
        return jsonify({"message": "El servicio asociado no existe", "status": 404}), 404
        
    # Obtener el número de servicio asociado
    numero_servicio = servicio.numero_servicio.split('-')[0]

    #Obtengo el ultimo subservicio del servicio asociado
    ultimo_sub_servicio = db.session.query(Sub_servicios).filter_by(servicio_id=id_servicio_bytes).order_by(Sub_servicios.numero_sub_servicio.desc()).first()

    if ultimo_sub_servicio:
        #Separo la cadena el numero del subservicio para obtener los ultimos dos digitos despues del guion
        ultimo_numero_subservicio = int(ultimo_sub_servicio.numero_sub_servicio.split('-')[1])
        nuevo_numero_subservicio = ultimo_numero_subservicio + 1

        if nuevo_numero_subservicio < 1 or nuevo_numero_subservicio > 99:
            return jsonify({"message": "El número de subservicio excede el rango permitido (01-99)", "status": 400}), 400
        
        if nuevo_numero_subservicio < 10: #Si el nuevo numero del subservicio es menor que 10 le agrego el 0 adelante
            numero_sub_serivico_formateado = f"{numero_servicio}-0{nuevo_numero_subservicio}"
        else:
            numero_sub_serivico_formateado = f"{numero_servicio}-{nuevo_numero_subservicio}"
        
        return numero_sub_serivico_formateado        
    else:
        numero_sub_serivico_formateado = f"{numero_servicio}-01"
        return numero_sub_serivico_formateado
         
    


