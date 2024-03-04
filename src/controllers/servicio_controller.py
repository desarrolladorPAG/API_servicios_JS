from flask import jsonify, request
from models.servicios import *
from controllers import cliente_general_controller
import uuid
import binascii
from sqlalchemy.exc import IntegrityError
from decouple import config
from models.tipo_clientes import Tipo_clientes
from models.clientes_generales import Clientes_generales
from models.usuarios import Usuarios
from models.tipo_intervenciones import Tipo_intervenciones
from sqlalchemy.orm import aliased

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

def obtener_servicios():
    try:
        lista = []
        UsuarioTecnico = aliased(Usuarios)
        UsuarioAdministrativo = aliased(Usuarios)

        servicios = db.session.query(
            Servicios.id_servicio, 
            Servicios.numero_servicio, 
            Servicios.fecha_solicitud, 
            Tipo_clientes.nombre_cliente, 
            Clientes_generales.nombre_cliente_general, 
            Servicios.nombre_solicitante, 
            Servicios.tipo_de_equipo, 
            Servicios.descripcion, 
            UsuarioTecnico.nombre_completo.label("tecnico_nombre"), 
            UsuarioAdministrativo.nombre_completo.label("administrativo_nombre"), 
            Servicios.id_activo,
            Tipo_intervenciones.nombre_tipo_intervencion).join(Tipo_clientes, Servicios.tipo_cliente_id == Tipo_clientes.id_tipo_cliente).join(Clientes_generales, Servicios.cliente_general_id == Clientes_generales.id_cliente_general, isouter=True).join(UsuarioTecnico, Servicios.tecnico_usuario_id == UsuarioTecnico.id_usuario).join(UsuarioAdministrativo, Servicios.administrativo_usuario_id == UsuarioAdministrativo.id_usuario).join(Tipo_intervenciones, Servicios.tipo_intervencion_id == Tipo_intervenciones.id_tipo_intervencion)
        
        for servicio in servicios:
            datos = {"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "numero_servicio" : servicio.numero_servicio, "fecha_solicitud" : servicio.fecha_solicitud.strftime('%d/%m/%y'), "tipo_cliente" : servicio.nombre_cliente, "cliente_general" : servicio.nombre_cliente_general, "solicitante" : servicio.nombre_solicitante, "tipo_de_equipo" : servicio.tipo_de_equipo, "descripcion" : servicio.descripcion, "tecnico_nombre" : servicio.tecnico_nombre, "administrativo_nombre" : servicio.administrativo_nombre, "id_activo" : servicio.id_activo, "tipo_intervencion" : servicio.nombre_tipo_intervencion}
            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def editar_servicio(id_servicio):
    try:
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        servicio = db.session.query(Servicios).get(id_servicio_bytes)

        if not servicio:
            return jsonify({"message" : "Servicio no encontrado", "status" : 404}) , 404

        tipo_cliente_id = request.json["tipo_cliente_id"]
        cliente_general_id = request.json["cliente_general_id"]

        if tipo_cliente_id == config('ID_CLIENTE_GENERAL'):
            if cliente_general_id == None: #Si no se selecciono un cliente general es porque creará uno
                nombre_cliente_general = request.json["nombre_cliente_general"]
                cliente_general_id_bytes = cliente_general_controller.crear_cliente_general(nombre_cliente_general)
                servicio.cliente_general_id = cliente_general_id_bytes
            else: #Si la variable cliente_general_id es diferente de nulo es porque escogio un cliente general ya creado
                cliente_general_id_bytes = binascii.unhexlify(cliente_general_id)
                servicio.cliente_general_id = cliente_general_id_bytes
        
        servicio.fecha_solicitud = request.json["fecha_solicitud"]
        servicio.tipo_cliente_id = binascii.unhexlify(tipo_cliente_id)
        servicio.nombre_solicitante = request.json["nombre_solicitante"]
        servicio.tipo_de_equipo = request.json["tipo_de_equipo"]
        servicio.descripcion = request.json["descripcion"]
        servicio.tecnico_usuario_id = binascii.unhexlify(request.json["tecnico_usuario_id"])
        servicio.administrativo_usuario_id = binascii.unhexlify(request.json["administrativo_usuario_id"])
        servicio.id_activo = request.json["id_activo"]
        servicio.tipo_intervencion_id = request.json["tipo_intervencion_id"]

        db.session.commit()
        return jsonify({"message" : "Servicio actualizado exitosamente", "status" : 200}) , 200
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500



        

