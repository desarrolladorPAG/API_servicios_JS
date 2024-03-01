from utils.db import db
from models.archivos_adjuntos import Archivos_adjuntos
from models.numeros_contables import Numeros_contables
from models.cierres_tecnicos import Cierres_tecnicos
from models.tipo_clientes import Tipo_clientes

class Sub_servicios(db.Model):
    __tablename__ = 'sub_servicios'
    id_sub_servicio = db.Column(db.BINARY(16), primary_key=True)
    servicio_id = db.Column(db.BINARY(16), db.ForeignKey('servicios.id_servicio'), nullable=False)
    tipo_cliente_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_clientes.id_tipo_cliente'), nullable=False)
    tipo_intervencion_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_intervenciones.id_tipo_intervencion'), nullable=False)
    tecnico_usuario_id = db.Column(db.BINARY(16), db.ForeignKey('usuarios.id_usuario'), nullable=False)
    administrativo_usuario_id = db.Column(db.BINARY(16), db.ForeignKey('usuarios.id_usuario'), nullable=False)
    numero_sub_servicio = db.Column(db.String(30),nullable = False)
    fecha_solicitud = db.Column(db.Date,nullable = False)
    nombre_solicitante = db.Column(db.String(45),nullable = False)
    descripcion = db.Column(db.String(255),nullable = False)

    archivos_adjuntos = db.relationship("Archivos_adjuntos", back_populates="sub_servicio",cascade="all,delete-orphan")
    numeros_contables = db.relationship("Numeros_contables", back_populates="sub_servicio",cascade="all,delete-orphan")
    cierres_tecnicos = db.relationship("Cierres_tecnicos", back_populates="sub_servicio",cascade="all,delete-orphan")

    #Relaciones de clave foraneas
    servicio = db.relationship('Servicios', back_populates="sub_servicios", uselist=False, single_parent=True)
    tipo_cliente = db.relationship('Tipo_clientes', back_populates="sub_servicios", uselist=False, single_parent=True)
    usuario = db.relationship('Usuarios', back_populates="sub_servicios", uselist=False, single_parent=True)
    tipo_intervencion = db.relationship('Tipo_intervenciones', back_populates="sub_servicios", uselist=False, single_parent=True)

    def __init__(self, id_sub_servicio, servicio_id, tipo_cliente_id, tipo_intervencion_id, tecnico_usuario_id, administrativo_usuario_id, numero_sub_servicio, fecha_solicitud, nombre_solicitante, descripcion) :
        self.id_sub_servicio = id_sub_servicio
        self.servicio_id = servicio_id
        self.tipo_cliente_id = tipo_cliente_id
        self.tipo_intervencion_id = tipo_intervencion_id
        self.tecnico_usuario_id = tecnico_usuario_id
        self.administrativo_usuario_id = administrativo_usuario_id
        self.numero_sub_servicio = numero_sub_servicio
        self.fecha_solicitud = fecha_solicitud
        self.nombre_solicitante = nombre_solicitante
        self.descripcion = descripcion
        

