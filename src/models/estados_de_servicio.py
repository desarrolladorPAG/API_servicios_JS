from utils.db import db

class Estados_de_servicio(db.Model):
     __tablename__ = 'estados_de_servicio'
     id_estado_servicio = db.Column(db.BINARY(16), primary_key=True)
     nombre_estado = db.Column(db.String(45),nullable = False)

     cierres_tecnicos = db.relationship("Cierres_tecnicos", back_populates="estado_servicio",cascade="all")

     def __init__(self, id_estado_servicio, nombre_estado):
          self.id_estado_servicio = id_estado_servicio
          self.nombre_estado = nombre_estado
          