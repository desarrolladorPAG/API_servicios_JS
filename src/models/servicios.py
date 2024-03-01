from utils.db import db
from models.sub_servicios import Sub_servicios
from models.clientes_generales import Clientes_generales
class Servicios(db.Model):
    __tablename__ = 'servicios'
    id_servicio = db.Column(db.BINARY(16), primary_key=True)
    numero_servicio = db.Column(db.String(30),nullable = False)
    fecha_solicitud = db.Column(db.Date,nullable = False)
    tipo_cliente_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_clientes.id_tipo_cliente'), nullable=False)
    cliente_general_id = db.Column(db.BINARY(16), db.ForeignKey('clientes_generales.id_cliente_general'), nullable=True)
    nombre_solicitante = db.Column(db.String(45),nullable = False)
    tipo_de_equipo = db.Column(db.String(255),nullable = False)
    descripcion = db.Column(db.String(255),nullable = False)
    tecnico_usuario_id = db.Column(db.BINARY(16), db.ForeignKey('usuarios.id_usuario'), nullable=False)
    administrativo_usuario_id = db.Column(db.BINARY(16), db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_activo = db.Column(db.String(50),nullable = False)
    tipo_intervencion_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_intervenciones.id_tipo_intervencion'), nullable=False)

    sub_servicios = db.relationship("Sub_servicios", back_populates="servicio",cascade="all,delete-orphan")
    archivos_adjuntos = db.relationship("Archivos_adjuntos", back_populates="servicio",cascade="all,delete-orphan")
    numeros_contables = db.relationship("Numeros_contables", back_populates="servicio",cascade="all,delete-orphan")
    cierres_tecnicos = db.relationship("Cierres_tecnicos", back_populates="servicio",cascade="all,delete-orphan")
    
    #Relaciones de clave foraneas
    tipo_cliente = db.relationship('Tipo_clientes', back_populates="servicios", uselist=False, single_parent=True)
    cliente_general = db.relationship('Clientes_generales', back_populates="servicios", uselist=False, single_parent=True)
    tecnico = db.relationship("Usuarios", foreign_keys=[tecnico_usuario_id])
    administrativo = db.relationship("Usuarios", foreign_keys=[administrativo_usuario_id])
    tipo_intervencion = db.relationship('Tipo_intervenciones', back_populates="servicios", uselist=False, single_parent=True)

    def __init__(self, id_servicio, numero_servicio, fecha_solicitud, tipo_cliente_id, cliente_general_id, nombre_solicitante, tipo_de_equipo, descripcion, tecnico_usuario_id, administrativo_usuario_id ,id_activo, tipo_intervencion_id):
        self.id_servicio = id_servicio
        self.numero_servicio = numero_servicio
        self.fecha_solicitud = fecha_solicitud
        self.tipo_cliente_id = tipo_cliente_id
        self.cliente_general_id = cliente_general_id
        self.nombre_solicitante = nombre_solicitante
        self.tipo_de_equipo = tipo_de_equipo
        self.descripcion = descripcion
        self.tecnico_usuario_id = tecnico_usuario_id
        self.administrativo_usuario_id = administrativo_usuario_id
        self.id_activo = id_activo
        self.tipo_intervencion_id = tipo_intervencion_id

    