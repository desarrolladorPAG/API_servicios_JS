from flask import jsonify, request
from models.usuarios import *
from flask_jwt_extended import create_access_token
import binascii

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
