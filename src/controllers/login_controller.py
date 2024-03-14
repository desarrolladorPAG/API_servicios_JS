from flask import jsonify, request
from models.usuarios import *
from flask_jwt_extended import create_access_token
import binascii
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from decouple import config
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from utils.mail import mail
from werkzeug.security import generate_password_hash

######################################### LOGIN NORMAL Y DE GOOGLE ##########################################
def login():
    try:
        correo = request.json['correo']
        password = request.json['password']

        usuario = db.session.query(Usuarios).filter_by(correo=correo).first()
        
        if usuario:
            if usuario.estado == 2 : # restriccion de que el usuario haya verificado su correo
                return jsonify({"message" : "Su cuenta no ha sido verificada, por favor ingrese a su correo y verifique su cuenta dandole clic al enlace que le enviamos" , "status" : 400}) , 400
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
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) }) , 500

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
            audience= config('ID_CLIENT'),
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
            rol_id = "5f8f6ab7f81a4251b48372e4f9d21526" # Por defecto al crearse el usuario tendrá rol de tecnico

            rol_id_bytes = binascii.unhexlify(rol_id)

            new_user = Usuarios(id_usuario,correo,None,nombre_completo, rol_id_bytes, 1)
            db.session.add(new_user)
            db.session.commit()

            id_user_new_hex = binascii.hexlify(id_usuario).decode()
            claims = {"rol_id" : rol_id, "nombre" : nombre_completo}
            access_token = create_access_token(identity=id_user_new_hex, additional_claims=claims)

            return jsonify({"token" : access_token, "message" : "Usuario creado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e) }) , 500

##################################### REGISTRAR USURIO Y VERIFICACION DE CORREO ################################3
def registro():
    try:
        correo = request.json["correo"]

        usuario = db.session.query(Usuarios).filter_by(correo=correo).first()

        if usuario:
            return jsonify({"message" : "El usuario ya existe" , "status" : 400}) , 400

        id_usuario = uuid.uuid4().bytes

        id_usuario_hex = binascii.hexlify(id_usuario).decode()
        token = generar_token(id_usuario_hex)
        enviar_correo_verificacion(correo, token)

        nombre_completo = request.json["nombre_completo"]
        password = request.json["password"]
        rol_id = binascii.unhexlify("5f8f6ab7f81a4251b48372e4f9d21526")
        password_encriptada = generate_password_hash(password,'pbkdf2:sha256',16)

        new_user = Usuarios(id_usuario, correo, password_encriptada, nombre_completo, rol_id, 2) #crear usuario con estado sin verificar

        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': f'Se ha enviado un link de verificación al correo: {correo}'}) ,200
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Error de integridad de la base de datos", "error": str(e)}), 400
    
    except Exception as e:
        if len(e.args) == 2:#Si el error tiene dos argumentos como los tiene la funcion de generar_token y enviar_correo_verificacion, mando el mensaje personalizado
            return jsonify({"message" : e.args[0], "error" : e.args[1]}) , 500 
        else:
            return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}), 500

def generar_token(id_usuario):
    try:
        serializer = URLSafeTimedSerializer(config('JWT_SECRET_KEY'))
        return serializer.dumps(id_usuario)
    except Exception as e:
        raise Exception("Error al generar el token", str(e))
        

def enviar_correo_verificacion(correo, token):
    try:
        mensaje = Message(subject='Verificación de correo electrónico',
                      recipients=[correo],
                      body=f'Por favor, haga clic en este enlace para verificar su correo electrónico: http://localhost:4200/verificar_correo/{token}', sender="sistema.pagcolombian@gmail.com")
        mail.send(mensaje)
    
    except Exception as e:
        raise Exception("Error al enviar el correo", str(e)) #Mando dos argumentos en el error para poder obtenerlos en la funcion que llame a esta funcion

def verificar_correo(token):
    try:
        serializer = URLSafeTimedSerializer(config('JWT_SECRET_KEY'))
        id_usuario = serializer.loads(token, max_age=3600)

        id_usuario_bytes = binascii.unhexlify(id_usuario)

        usuario = db.session.query(Usuarios).filter_by(id_usuario = id_usuario_bytes).first()

        if not usuario:
            return jsonify({"message" : "Usuario no encontrado", "status" : 404 }) , 404
        elif usuario.estado == 1:
            return jsonify({"message" : "Su correo ya ha sido verificado, por favor inicie sesión", "status" : 400 }) , 400
            
        
        usuario.estado = 1 #Cambio el estado de sin verificar a activo
        db.session.commit()

        return jsonify({'message': 'Correo electrónico verificado correctamente' , "status" : 200}) , 200
    
    except SignatureExpired:
        db.session.rollback()
        return jsonify({'message': 'El link de verificación ha expirado, por favor reenvie uno nuevo'}) , 400
    
    except BadSignature:
        db.session.rollback()
        return jsonify({'message': 'El link de verificación es inválido, reenvie uno nuevo o comuniquese con el administrador'}) , 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "Error al verificar el correo, por favor reenvie un nuevo link o comuniquese con el administrador", "error" : str(e) }) , 500

def reenviar_link_verificacion():
    try:
        correo = request.json["correo"]
        usuario = db.session.query(Usuarios).filter_by(correo=correo).first()

        if not usuario:
            return jsonify({"message" : "Usuario no encontrado, por favor registrese", "status" : 404 }) , 404
        
        if usuario.estado == 1:
            return jsonify({"message" : "El correo ya ha sido verificado, por favor inicie sesión", "status" : 400 }) , 400

        id_usuario_hex = binascii.hexlify(usuario.id_usuario).decode()
        token = generar_token(id_usuario_hex)
        enviar_correo_verificacion(correo, token)

        return jsonify({'message': f'Se ha enviado un nuevo link de verificación al correo: {correo}'}) ,200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)}), 500








