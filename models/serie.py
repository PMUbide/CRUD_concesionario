# De util.db importa el db para pasarle el modelo.
from utils.db import db

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    # Se especifica que propiedad es la clave foránea en  la relación
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    #Relación con tabla-child - borrará todos los vehiculos de la serie al borrar la serie
    vehiculos = db.relationship("Vehiculo", backref="serie", cascade="all, delete-orphan")

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Serie ({self.nombre})"

    def __str__(self):
        return self.nombre