from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.serie import Serie

from models.vehiculo import Vehiculo
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
vehiculos = Blueprint("vehiculos", __name__)



@vehiculos.route("/vehiculos/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    series = Serie.query.all()
    vehiculos = Vehiculo.query.all()

    return render_template("vehiculos/index.html", series=series, vehiculos= vehiculos)


@vehiculos.route("/vehiculos/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    matricula = request.form["matricula"]
    color = request.form["color"]
    serie_id = request.form["serie_id"]

    # Nuevo objeto para guardar
    new_vehiculo = Vehiculo(matricula, color)

    serie = Serie.query.get(serie_id)
    serie.vehiculos.append(new_vehiculo)

    db.session.add(new_vehiculo)

    # Ahora se acaba con la conexión y se hace commit
    db.session.commit()

    # Antes de reenviar, guardamos algo en la funcion flash
    flash("Vehículo añadido satisfactoriamente!")

    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))


@vehiculos.route("/vehiculos/busqueda", methods=["POST"])
def search():

    matricula = request.form["matricula2"]

    series = Serie.query.all()
    results = []
    encontrado = Vehiculo.query.filter_by(matricula=matricula).first()
    if encontrado != None:
        results.append(Vehiculo.query.filter_by(matricula=matricula).first())

    # return redirect(url_for('vehiculos.index'))
    return render_template("vehiculos/index.html", series=series, vehiculos= results)
