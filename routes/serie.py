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


    db.session.add(new_serie)

    # Ahora se acaba con la conexión y se hace commit
    db.session.commit()

    # Antes de reenviar, guardamos algo en la funcion flash
    flash("Serie añadido satisfactoriamente!")

    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))


@series.route("/series/update/<id>", methods=["POST", "GET"])
def update(id):
    serie = Serie.query.get(id)
    marcas = Marca.query.all()

    if request.method == 'POST':
        serie.nombre = request.form["nombre"]
        valor = request.form["marca_id"]

        if(valor != 'None'):
            serie.marca_id = request.form["marca_id"]
        

        db.session.commit()
        flash("Serie updateado satisfactoriamente!")
        return redirect(url_for('series.index'))

    return render_template('series/update.html', serie=serie, marcas=marcas)

# Espera un id 
@series.route("/series/delete/<id>", methods=["POST", "GET"])
def delete(id):

    serie = Serie.query.get(id)

    if request.method == 'POST':
        db.session.delete(serie)
        db.session.commit()
        flash("Serie borrado satisfactoriamente!")
        return redirect(url_for('series.index'))

    return render_template('series/delete.html', serie=serie)
    
