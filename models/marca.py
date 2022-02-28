# De util.db importa el db para pasarle el modelo.
from utils.db import db


class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    series = db.relationship("Serie", backref="marca")

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Marca ({self.nombre})"

    # Lo que devolverá al elemento hijo
    def __str__(self):
        return self.nombre

