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

    # Comprobar si existe ese registro SOLO POR MATRICULA
    records = db.session.query(Vehiculo).filter_by(matricula=matricula).first()
    if records == None:

        # Comprobar si no está vacía la matricula
        if(matricula != ""):

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
            return redirect(url_for('vehiculos.index'))

        return redirect(url_for('vehiculos.index')) 

    flash("Ese elemento ya existe")
    return redirect(url_for('vehiculos.index'))    



@vehiculos.route("/vehiculos/busqueda", methods=["POST"])
def search():

    matricula2 = request.form["matricula2"]
    serie_busqueda = request.form["serie_busqueda"]

    # Si no ha introducido nada en la búsqueda
    if matricula2 == '' and serie_busqueda == 'None':
        return redirect(url_for('vehiculos.index'))
    
    todos = Vehiculo.query.filter(Vehiculo.matricula.like(matricula2).first())

    if(serie_busqueda != 'None'):
        todos = Vehiculo.query.filter(Vehiculo.serie_id.like(serie_busqueda)).all()

    series = Serie.query.all()
    results = []
    
    if todos != None:
        results.append(todos)

    # return redirect(url_for('vehiculos.index'))
    return render_template("vehiculos/index.html", series=series, vehiculos= todos)


@vehiculos.route("/vehiculos/busqueda_matricula", methods=["POST"])
def search_matricula():

    matricula2 = request.form["matricula2"]
    
    # Si no ha introducido nada en la búsqueda
    if matricula2 == '' :
        return redirect(url_for('vehiculos.index'))

    records = db.session.query(Vehiculo).filter_by(matricula=matricula2).first()

    series = Serie.query.all()
    results = []
    
    if records != None:
        results.append(records)

    # Creamos una lista que siempre contiene todos los vehículos para el autocompletar de la vista
    vehiculos_total = Vehiculo.query.all()

    # return redirect(url_for('vehiculos.index'))
    return render_template("vehiculos/index.html", series=series, vehiculos= results, vehiculos_total=vehiculos_total)


@vehiculos.route("/vehiculos/busqueda_serie", methods=["POST"])
def search_serie():

    serie_busqueda = request.form["serie_busqueda"]
    # Si no ha introducido nada en la búsqueda
    if serie_busqueda == 'None':
        return redirect(url_for('vehiculos.index'))

    records = db.session.query(Vehiculo).filter_by(serie_id=serie_busqueda).all()

    series = Serie.query.all()

    # Creamos una lista que siempre contiene todos los vehículos para el autocompletar de la vista
    vehiculos_total = Vehiculo.query.all()
    
    # return redirect(url_for('vehiculos.index'))
    return render_template("vehiculos/index.html", series=series, vehiculos= records, vehiculos_total=vehiculos_total)


# Espera un id 
@vehiculos.route("/vehiculos/delete/<id>", methods=["POST", "GET"])
def delete(id):

    vehiculo = Vehiculo.query.get(id)

    if request.method == 'POST':
        db.session.delete(vehiculo)
        db.session.commit()
        flash("Vehiculo borrado satisfactoriamente!")
        return redirect(url_for('vehiculos.index'))

    return render_template('vehiculos/delete.html', vehiculo=vehiculo)



@vehiculos.route("/vehiculos/update/<id>", methods=["POST", "GET"])
def update(id):
    vehiculo = Vehiculo.query.get(id)
    series = Serie.query.all()

    if request.method == 'POST':
        # Recoger valores del formulario
        matricula = request.form["matricula"]
        color = request.form["color"]
        valor = request.form["serie_id"]

        #Si el nombre no está vacío
        if (matricula != ""):
            # Si no ha introducido valor asignaremos el que tenía ya
            if(valor == 'None'):
                serie_id = vehiculo.serie_id
            else:
                serie_id = valor        
            # Comprobar si existe ese registro 
            records = db.session.query(Vehiculo).filter_by(matricula=matricula).first()
            #Comprobar si no está vacío
            if(records == None or records.id == int(id)):
                vehiculo.matricula = matricula
                vehiculo.color = color
                vehiculo.serie_id = int(serie_id)
                db.session.commit()
                flash("Vehiculo updateado satisfactoriamente!")
                return redirect(url_for('vehiculos.index'))
            flash("Ese elemento ya existe!")    

    return render_template('vehiculos/update.html', series=series, vehiculo=vehiculo)