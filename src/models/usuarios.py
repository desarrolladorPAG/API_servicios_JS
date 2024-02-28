from utils.db import db
from models.servicios import Servicios

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.BINARY(16), primary_key=True)
    correo = db.Column(db.String(255),nullable = False)
    password = db.Column(db.String(255))
    nombre_completo = db.Column(db.String(50))
    rol_id = db.Column(db.BINARY(16), db.ForeignKey('roles.id_rol'), nullable=False)

    servicios = db.relationship("Servicios", back_populates="usuario",cascade="all")
    sub_servicios = db.relationship("Sub_servicios", back_populates="usuario",cascade="all")

    #Relaciones de clave foraneas
    rol = db.relationship('Roles', back_populates="usuarios", uselist=False, single_parent=True)

    def __init__(self, id_usuario, correo, password, nombre_completo, rol_id):
        self.id_usuario = id_usuario
        self.correo = correo
        self.password = password
        self.nombre_completo = nombre_completo
        self.rol_id = rol_id
        