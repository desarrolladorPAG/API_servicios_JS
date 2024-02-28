from utils.db import db

class Tipo_intervenciones(db.Model):
    __tablename__ = 'tipo_intervenciones'
    id_tipo_intervencion= db.Column(db.BINARY(16), primary_key=True)
    tipo_cliente_id = db.Column(db.BINARY(16), db.ForeignKey('tipo_clientes.id_tipo_cliente'), nullable=False)
    nombre_tipo_intervencion = db.Column(db.String(45),nullable = False)

    servicios = db.relationship("Servicios", back_populates="tipo_intervencion",cascade="all")
    sub_servicios = db.relationship("Sub_servicios", back_populates="tipo_intervencion",cascade="all")

    #Relaciones de clave foraneas
    tipo_cliente = db.relationship('Tipo_clientes', back_populates="tipo_intervenciones", uselist=False, single_parent=True)

    def __init__(self, id_tipo_intervencion, tipo_cliente_id, nombre_tipo_intervencion):
        self.id_tipo_intervencion = id_tipo_intervencion
        self.tipo_cliente_id = tipo_cliente_id
        self.nombre_tipo_intervencion = nombre_tipo_intervencion
        