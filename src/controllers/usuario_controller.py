from flask import jsonify, request
from models.usuarios import *
import uuid
import binascii
from werkzeug.security import generate_password_hash

def crear_usuario():
    try:
        id_usuario = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        correo = request.json['correo']
        password = request.json['password']
        nombre_completo = request.json['nombre_completo']
        rol_id = request.json['rol_id']

        rol_id_bytes = binascii.unhexlify(rol_id) #El rol_id de hexadecimal a binario

        usuario = db.session.query(Usuarios).filter_by(correo = correo).first()

        if not usuario:
            password_encriptada = generate_password_hash(password,'pbkdf2:sha256',16)

            new_usuario = Usuarios(id_usuario, correo, password_encriptada, nombre_completo, rol_id_bytes)
            db.session.add(new_usuario)
            db.session.commit()

            return jsonify({"message" : "Usuario creado correctamente", "status" : 200}) , 200
        
        else:
            return jsonify({"message": "El usuario ya se encuentra registrado", "status" : 400}) , 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

def obtener_usuarios():
    try:
        lista = []
        usuarios = db.session.query(Usuarios).all()

        for usuario in usuarios:
            datos = {"id_usuario" : binascii.hexlify(usuario.id_usuario).decode(), "correo" : usuario.correo, "nombre" : usuario.nombre_completo, "rol_id" : binascii.hexlify(usuario.rol_id).decode()}
            lista.append(datos)
        
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}) , 500

