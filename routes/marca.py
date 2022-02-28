from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.marca import Marca
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
marcas = Blueprint("marcas", __name__)



@marcas.route("/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    marcas = Marca.query.all()
    return render_template("marcas/index.html", marcas=marcas)



@marcas.route("/marcas/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    nombre = request.form["nombre"]

    # Nuevo objeto para guardar
    new_marca = Marca(nombre)

    # Funciones para guardar en la base 
    db.session.add(new_marca)
    # Ahora se acaba con la conexión y se hace commit
    db.session.commit()

    # Antes de reenviar, guardamos algo en la funcion flash
    flash("Marca añadido satisfactoriamente!")

    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))