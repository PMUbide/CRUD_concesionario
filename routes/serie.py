from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.marca import Marca

from models.serie import Serie
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
series = Blueprint("series", __name__)



@series.route("/series/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    series = Serie.query.all()
    marcas = Marca.query.all()
    return render_template("series/index.html", series=series, marcas = marcas )


@series.route("/series/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    nombre = request.form["nombre"]
    marca_id = request.form["marca_id"]

    print(marca_id)
    # Nuevo objeto para guardar
    new_serie = Serie(nombre)

    marca = Marca.query.get(marca_id)
    marca.series.append(new_serie)

    new_serie.marca


    db.session.add(new_serie)

    # Ahora se acaba con la conexión y se hace commit
    db.session.commit()

    # Antes de reenviar, guardamos algo en la funcion flash
    flash("Serie añadido satisfactoriamente!")

    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))