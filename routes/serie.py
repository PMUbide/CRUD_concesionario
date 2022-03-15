#Imports de flask y componentes necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlalchemy
from models.marca import Marca
from models.serie import Serie
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
series = Blueprint("series", __name__)


# Método que devuelve la vista de la lista de series 
@series.route("/series/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    series = Serie.query.all()
    # Guarda las marcas porque serán necesarias para crear elementos nuevos
    marcas = Marca.query.all()
    # Función para renderizar el template con las variables que se le envían
    return render_template("series/index.html", series=series, marcas = marcas )

# Método que se ejecuta cuando se guarda una nueva serie en la bbdd
@series.route("/series/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    nombre = request.form["nombre"]
    marca_id = request.form["marca_id"]
    # Comprobar si existe ese nombre ya
    # Se comprueba por nombre y por marca
    records = db.session.query(Serie).filter_by(nombre=nombre, marca_id=marca_id).first()
    if records == None:
        if nombre != "":
            # Nuevo objeto para guardar
            new_serie = Serie(nombre)
            # Añadirle a la marca que tenga ese id el elemento de serie
            marca = Marca.query.get(marca_id)
            marca.series.append(new_serie)
            # añadido a la bbdd
            db.session.add(new_serie)
            # Ahora se acaba con la conexión y se hace commit
            db.session.commit()
            # Antes de reenviar, guardamos algo en la funcion flash
            flash("Serie añadido satisfactoriamente!")
            # Función de flask para hacer redirecciones 
        return redirect(url_for('series.index'))       
    # Mensaje de redireccón si ya existe
    flash("Ese elemento ya existe")
    # Redirección al index de series
    return redirect(url_for('series.index'))    

# Método para hacer un update de un elemento.
# Acepta los métodos de GET para llevar a la viste del update con el objeto,
# También el método POST cuando se haya ejecutado la opción de update del formulario.
@series.route("/series/update/<id>", methods=["POST", "GET"])
def update(id):
    #Guardamos en un objeto serie con el id recibido
    serie = Serie.query.get(id)
    # Guardamos la lista de marcas
    marcas = Marca.query.all()
    # Si le llega como POST proceder al update
    if request.method == 'POST':
        # Recoger valores del formulario
        nombre = request.form["nombre"]
        valor = request.form["marca_id"]
        #Si el nombre no está vacío
        if (nombre != ""):
            # Si no ha introducido valor en la marca_id asignaremos el que tenía ya
            if(valor == 'None'):
                marca_id = serie.marca_id
            else:
                marca_id = valor        
            # Comprobar si existe ese registro  por nombre y por marca_id
            records = db.session.query(Serie).filter_by(nombre=nombre, marca_id=marca_id).first()
            #Comprobar si no está vacío
            if(records == None):
                # Aplicarle los cambios al objeto
                serie.nombre = nombre
                serie.marca_id = marca_id
                # Guardado de la session de la bbdd
                db.session.commit()
                # guardamos mensaje en la funcion flash
                flash("Serie updateado satisfactoriamente!")
                # Función de flask para hacer redirecciones 
                return redirect(url_for('series.index'))
            flash("Ese elemento ya existe!")    
    # Si llega como GET hará redirección a la vista de udpate con lo necesario
    return render_template('series/update.html', serie=serie, marcas=marcas)

# Función para eliminar un registro. Espera un id para hacer el delete
# Puede ser GET la primera vez que se ejecute para ir a la vista de confirmación de delete,
# Si se le da a SI en la vista de confirmación, entrará como método POST
@series.route("/series/delete/<id>", methods=["POST", "GET"])
def delete(id):
    # Guardamos el objeto que tenga ese id
    serie = Serie.query.get(id)
    # Si llega como POST se procede a la eliminación
    if request.method == 'POST':
        # Método delete de objeto de la bdd
        db.session.delete(serie)
        # Session commit para guardar los cambios
        db.session.commit()
        # Envio del mensaje al html
        flash("Serie borrado satisfactoriamente!")
        # Función para hacer redirección de flask
        return redirect(url_for('series.index'))
    # Si llega como GET hará la redirección a la vista de confirmar delete
    return render_template('series/delete.html', serie=serie)
    
