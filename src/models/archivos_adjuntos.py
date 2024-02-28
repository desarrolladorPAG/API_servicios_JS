from utils.db import db
from models.tipo_adjuntos import Tipo_adjuntos
class Archivos_adjuntos(db.Model):
    __tablename__ = 'archivos_adjuntos'
    id_archivo_adjunto = db.Column(db.BINARY(16), primary_key=True)
    servicio_id = db.Column(db.BINARY(16), db.ForeignKey('servicios.id_servicio'), nullable=True)
    sub_servicio_id = db.Column(db.BINARY(16), db.ForeignKey('sub_servicios.id_sub_servicio'), nullable=True)
    tipo_adjunto_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_adjuntos.id_tipo_adjunto'), nullable=True)
    ruta_archivo = db.Column(db.String(255),nullable = False)

    #Relaciones de llaves foraneas
    servicio = db.relationship('Servicios', back_populates="archivos_adjuntos", uselist=False, single_parent=True)
    sub_servicio = db.relationship('Sub_servicios', back_populates="archivos_adjuntos", uselist=False, single_parent=True)
    tipo_adjunto = db.relationship('Tipo_adjuntos', back_populates="archivos_adjuntos", uselist=False, single_parent=True)

    def __init__(self, id_archivo_adjunto, servicio_id, sub_servicio_id, tipo_adjunto_id, ruta_archivo):
        self.id_archivo_adjunto = id_archivo_adjunto
        self.servicio_id = servicio_id
        self.sub_servicio_id = sub_servicio_id
        self.tipo_adjunto_id = tipo_adjunto_id
        self.ruta_archivo = ruta_archivo

