# De util.db importa el db para pasarle el modelo.
from utils.db import db


class Vehiculo(db.Model):
    __searchable__ = ['matricula']
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(100))
    color = db.Column(db.String(100))
    #specify which property is the foreign key in a relationship
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))

    def __init__(self, matricula, color):
        self.matricula = matricula
        self.color = color

    def __repr__(self):
        return f"Vehiculo ({self.matricula})"

    def __str__(self):
        return self.matricula