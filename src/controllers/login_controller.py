from flask import jsonify, request
from models.usuarios import *
from flask_jwt_extended import create_access_token
import binascii
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config

def login():
    try:
        correo = request.json['correo']
        password = request.json['password']

        usuario = db.session.query(Usuarios).filter_by(correo=correo).first()
        
        if usuario:
            if usuario.verificar_password(password):
                id_usuario_hex = binascii.hexlify(usuario.id_usuario).decode() #El id del usuario lo convierto a hexadecimal
                rol_id = binascii.hexlify(usuario.rol_id).decode()
                claims = {"rol_id" : rol_id, "nombre" : usuario.nombre_completo}
                access_token = create_access_token(identity=id_usuario_hex, additional_claims=claims)
                return jsonify({"token" : access_token})
            else :
                return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 400}) , 400
        else:
            return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 400}) , 400
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) })

def login_google():
    try:
        info_usuario = validar_token_acceso_google(request.json["token_google"])

        token = crear_usuario_de_google(info_usuario)

        return token
    
    except ValueError as e:
        return jsonify({"message" : "Token no válido", "error" : str(e) }) , 401
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) }) , 500

def validar_token_acceso_google(token_google):
    try:
        # Verificar el token de acceso con las claves públicas de Google
        info_usuario = id_token.verify_oauth2_token(
            token_google,
            requests.Request(),
            audience= config('ID_CLIENT'), #NO HAY ID_CLIENT EN EL ARCHIVO .ENV
            clock_skew_in_seconds= 10
        )

        # Si el token es válido, devolver la información del usuario
        return info_usuario
    
    except ValueError as e:
        # El token no es válido
        raise ValueError(str(e))

def crear_usuario_de_google(info_usuario):
    try:
        correo = info_usuario["email"]
    
        usuario = db.session.query(Usuarios).filter_by(correo=correo).first()
        

        if usuario: #Si existe el usuario le devuelvo un token con sus datos
            id_user_hex = binascii.hexlify(usuario.id_usuario).decode()
            rol_id = binascii.hexlify(usuario.rol_id).decode()
            claims = {"rol_id" : rol_id, "nombre" : usuario.nombre_completo}
            access_token = create_access_token(identity=id_user_hex, additional_claims=claims)                
            return jsonify({"token" : access_token}) , 200
        
        else: #Si no existe el usuario se registra en la bd y se e da el token
            id_usuario = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
            nombre_completo = info_usuario["name"]
            rol_id = "" # Por defecto al crearse el usuario tendrá rol de tecnico

            new_user = Usuarios(id_usuario,correo,None,nombre_completo, rol_id)
            db.session.add(new_user)
            db.session.commit()

            id_user_new_hex = binascii.hexlify(id_usuario).decode()
            claims = {"rol_id" : rol_id, "nombre" : nombre_completo}
            access_token = create_access_token(identity=id_user_new_hex, additional_claims=claims)

            return jsonify({"token" : access_token, "message" : "Usuario creado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e) })
