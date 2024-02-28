from utils.db import db

class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.BINARY(16), primary_key=True)
    nombre_rol = db.Column(db.String(45),nullable = False)

    usuarios = db.relationship("Usuarios", back_populates="rol",cascade="all")

    def __init__(self, id_rol, nombre_rol):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol
        