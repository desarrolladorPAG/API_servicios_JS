from utils.db import db

class Tipo_clientes(db.Model):
    __tablename__ = 'tipo_clientes'
    id_tipo_cliente= db.Column(db.BINARY(16), primary_key=True)
    nombre_cliente = db.Column(db.String(45),nullable = False)

    servicios = db.relationship("Servicios", back_populates="tipo_cliente",cascade="all")
    sub_servicios = db.relationship("Sub_servicios", back_populates="tipo_cliente",cascade="all")
    tipo_intervenciones = db.relationship("Tipo_intervenciones", back_populates="tipo_cliente",cascade="all")

    def __init__(self, id_tipo_cliente, nombre_cliente):
        self.id_tipo_cliente = id_tipo_cliente
        self.nombre_cliente = nombre_cliente
        