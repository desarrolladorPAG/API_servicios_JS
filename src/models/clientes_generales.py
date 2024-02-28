from utils.db import db

class Clientes_generales(db.Model):
    __tablename__ = 'clientes_generales'
    id_cliente_general = db.Column(db.BINARY(16), primary_key=True)
    nombre_cliente_general = db.Column(db.String(45),nullable = False)

    servicios = db.relationship("Servicios", back_populates="cliente_general",cascade="all")

    def __init__(self, id_cliente_general, nombre_cliente_general):
        self.id_cliente_general = id_cliente_general
        self.nombre_cliente_general = nombre_cliente_general
        