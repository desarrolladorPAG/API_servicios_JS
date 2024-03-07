from utils.db import db
from models.estados_de_servicio import Estados_de_servicio

class Cierres_tecnicos(db.Model):
    __tablename__ = 'cierres_tecnicos'
    id_cierre_tecnico = db.Column(db.BINARY(16), primary_key=True)
    servicio_id = db.Column(db.BINARY(16), db.ForeignKey('servicios.id_servicio'), nullable=True)
    sub_servicio_id = db.Column(db.BINARY(16), db.ForeignKey('sub_servicios.id_sub_servicio'), nullable=True)
    fecha_cierre = db.Column(db.Date,nullable = False)
    estado_servicio_id = db.Column(db.BINARY(16), db.ForeignKey('estados_de_servicio.id_estado_servicio'), nullable=False)
    usuario_id = db.Column(db.BINARY(16), db.ForeignKey('usuarios.id_usuario'), nullable=False)
    descripcion = db.Column(db.String(255),nullable = False)

    #Relaciones de llaves foraneas
    servicio = db.relationship('Servicios', back_populates="cierres_tecnicos", uselist=False, single_parent=True)
    sub_servicio = db.relationship('Sub_servicios', back_populates="cierres_tecnicos", uselist=False, single_parent=True)
    estado_servicio = db.relationship('Estados_de_servicio', back_populates="cierres_tecnicos", uselist=False, single_parent=True)
    usuario = db.relationship('Usuarios', back_populates="cierres_tecnicos", uselist=False, single_parent=True)

    def __init__(self, id_cierre_tecnico, servicio_id, sub_servicio_id, fecha_cierre, estado_servicio_id, usuario_id, descripcion):
        self.id_cierre_tecnico = id_cierre_tecnico
        self.servicio_id = servicio_id
        self.sub_servicio_id = sub_servicio_id
        self.fecha_cierre = fecha_cierre
        self.estado_servicio_id = estado_servicio_id
        self.usuario_id = usuario_id
        self.descripcion = descripcion

        
