from utils.db import db

class Tipo_adjuntos(db.Model):
    __tablename__ = 'tipo_adjuntos'
    id_tipo_adjunto = db.Column(db.BINARY(16), primary_key=True)
    nombre_tipo = db.Column(db.String(45),nullable = False)

    archivos_adjuntos = db.relationship("Archivos_adjuntos", back_populates="tipo_adjunto",cascade="all")

    def __init__(self, id_tipo_adjunto, nombre_tipo):
        self.id_tipo_adjunto = id_tipo_adjunto
        self.nombre_tipo = nombre_tipo
        