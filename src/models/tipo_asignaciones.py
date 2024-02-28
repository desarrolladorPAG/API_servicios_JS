from utils.db import db

class Tipo_asignaciones(db.Model):
    __tablename__ = 'tipo_asignaciones'
    id_tipo_asignacion = db.Column(db.BINARY(16), primary_key=True)
    nombre_asignacion = db.Column(db.String(45),nullable = False)

    numeros_contables = db.relationship("Numeros_contables", back_populates="tipo_asignacion",cascade="all")

    def __init__(self, id_tipo_asignacion, nombre_asignacion):
        self.id_tipo_asignacion = id_tipo_asignacion
        self.nombre_asignacion = nombre_asignacion
        