from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlalchemy

from models.marca import Marca
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
marcas = Blueprint("marcas", __name__)

def arreglaNombre(nombre):
    # Quitar espacios despues
    name = ''
    # Comprobar si tiene espacios el nombre, y gestionarlos por separado las mayusculas
    nombre_separado = nombre.split(" ")
    for n in nombre_separado:
        n = f'{n[0:1].capitalize()}{n[1:].lower()}'
        name += f'{n} '
    # Quitarle espacios por detrás    
    name = name.rstrip()    
    return name


@marcas.route("/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    marcas = Marca.query.all()
    return render_template("marcas/index.html", marcas=marcas)



@marcas.route("/marcas/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    nombre = request.form["nombre"]
    #Comprobar que no exista anteriormente
    try:
        # If para evitar que cree un registro vacío
        if(nombre != ''):
            nombre = arreglaNombre(nombre)
            # Nuevo objeto para guardar
            new_marca = Marca(nombre)
            # Funciones para guardar en la base 
            db.session.add(new_marca)
            # Ahora se acaba con la conexión y se hace commit
            db.session.commit()
            # Antes de reenviar, guardamos algo en la funcion flash
            flash("Marca añadido satisfactoriamente!")
    except sqlalchemy.exc.IntegrityError:
        flash("Ese elemento ya existe")
    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))


# Espera un id 
@marcas.route("/marcas/delete/<id>", methods=["POST", "GET"])
def delete(id):

    marca = Marca.query.get(id)

    if request.method == 'POST':
        db.session.delete(marca)
        db.session.commit()
        flash("Marca borrado satisfactoriamente!")
        return redirect(url_for('marcas.index'))

    return render_template('marcas/delete.html', marca=marca)


@marcas.route("/marcas/update/<id>", methods=["POST", "GET"])
def update(id):
    marca = Marca.query.get(id)

    if request.method == 'POST':
        nombre = request.form["nombre"]
        if(nombre != ""):
            nombre = arreglaNombre(nombre)
            # Comprobar si existe ese nombre ya
            records = db.session.query(Marca).filter_by(nombre=nombre).first()
            #Si no existe hará el update
            if(records == None):
                marca.nombre = nombre
                db.session.commit()
                flash("Marca updateado satisfactoriamente!")
                return redirect(url_for('marcas.index'))
            else:
                flash("Error al hacer update elemento ya existe")
    return render_template('marcas/update.html', marca=marca)



