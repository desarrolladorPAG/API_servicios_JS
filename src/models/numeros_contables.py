from utils.db import db

class Numeros_contables(db.Model):
    __tablename__ = 'archivos_adjuntos'
    id_numero_contable = db.Column(db.BINARY(16), primary_key=True)
    servicio_id = db.Column(db.BINARY(16), db.ForeignKey('servicios.id_servicio'), nullable=True)
    sub_servicio_id = db.Column(db.BINARY(16), db.ForeignKey('sub_servicios.id_sub_servicio'), nullable=True)
    tipo_asignacion_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_asignaciones.id_tipo_asignacion'), nullable=False)
    numero_documento = db.Column(db.String(50),nullable = False)
    fecha_emision = db.Column(db.Date,nullable = False)
    ruta_archivo = db.Column(db.String(255),nullable = False)
    observacion = db.Column(db.String(255),nullable = True)

    #Relaciones de llaves foraneas
    servicio = db.relationship('Servicios', back_populates="numeros_contables", uselist=False, single_parent=True)
    sub_servicio = db.relationship('Sub_servicios', back_populates="numeros_contables", uselist=False, single_parent=True)
    tipo_asignacion = db.relationship('Tipo_asignaciones', back_populates="numeros_contables", uselist=False, single_parent=True)

    def __init__(self, id_numero_contable, servicio_id, sub_servicio_id, tipo_asignacion_id, numero_documento, fecha_emision, ruta_archivo, observacion):
        self.id_numero_contable = id_numero_contable
        self.servicio_id = servicio_id
        self.sub_servicio_id = sub_servicio_id
        self.tipo_asignacion_id = tipo_asignacion_id
        self.numero_documento = numero_documento
        self.fecha_emision = fecha_emision
        self.ruta_archivo = ruta_archivo
        self.observacion = observacion
        
