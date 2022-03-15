#Imports de flask y componentes necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlalchemy
from models.marca import Marca
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
marcas = Blueprint("marcas", __name__)

# método que recibe un string y lo devuelve con la primera letra en mayúscula.
# Si tiene espacios lo gestiona y aplica la mayúscula a cada elemento.
def arreglaNombre(nombre):
    name = ''
    # Comprobar si tiene espacios el nombre, y gestionarlos por separado las mayusculas
    nombre_separado = nombre.split(" ")
    for n in nombre_separado:
        n = f'{n[0:1].capitalize()}{n[1:].lower()}'
        name += f'{n} '
    # Quitarle espacios por detrás    
    name = name.rstrip()    
    return name

# Método que devuelve la primera vista de la app con el index.html
@marcas.route("/")
def index():
    # Guarda la lista en una variable de lista, y la lleva al template
    marcas = Marca.query.all()
    return render_template("marcas/index.html", marcas=marcas)

# Método que se ejecuta cuando se guarda una nueva marca en la bbdd
@marcas.route("/marcas/new", methods=["POST"])
def add():
    # Con request saca el valor Flask del form del template
    nombre = request.form["nombre"]
    #Comprobar que no exista anteriormente
    try:
        # If para evitar que cree un registro vacío
        if(nombre != ''):
            # LLamar a función para dejar el string en el formato adecuado
            nombre = arreglaNombre(nombre)
            # Nuevo objeto para guardar
            new_marca = Marca(nombre)
            # Funciones para guardar en la base 
            db.session.add(new_marca)
            # Ahora se acaba con la conexión y se hace commit para guardar los cambios
            db.session.commit()
            # Antes de reenviar, guardamos algo en la funcion flash que mostrará en la página un mensaje
            flash("Marca añadido satisfactoriamente!")
    # Si intenta crear un elemento que ya existe, debido a que es Unique=True devuelve un error.        
    except sqlalchemy.exc.IntegrityError:
        flash("Ese elemento ya existe")
    # Función de flask para hacer redirecciones 
    return redirect(url_for('marcas.index'))


# Función para eliminar un registro. Espera un id para hacer el delete
# Puede ser GET la primera vez que se ejecute para ir a la vista de confirmación de delete,
# Si se le da a SI en la vista de confirmación, entrará como método POST
@marcas.route("/marcas/delete/<id>", methods=["POST", "GET"])
def delete(id):
    # Guardamos el elemento haciendo la búsqueda a la bdd
    marca = Marca.query.get(id)
    # Si el método es post procede a eliminarlo
    if request.method == 'POST':
        # Método para eliminar del objeto de la bbdd
        db.session.delete(marca)
        # Guardamos la session
        db.session.commit()
        # Añadimos mensaje para enviar a la vista
        flash("Marca borrado satisfactoriamente!")
        # Función de flask para ahcer redirecciones
        return redirect(url_for('marcas.index'))
    # Si no es post reenvía a la vista de confirmar delete con el objeto.
    return render_template('marcas/delete.html', marca=marca)

# Método para hacer un update de un elemento.
# Acepta los métodos de GET para llevar a la viste del update con el objeto,
# También el método POST cuando se haya ejecutado la opción de update del formulario.
@marcas.route("/marcas/update/<id>", methods=["POST", "GET"])
def update(id):
    # Guardamos el elemento haciendo la búsqueda a la bdd
    marca = Marca.query.get(id)
     # Si el método es post procede a hacer el update
    if request.method == 'POST':
        # REcoge el elemento del form con una función de flask
        nombre = request.form["nombre"]
        # Si no está vacío
        if(nombre != ""):
            # Método para arreglar aplicarle el formato correcto
            nombre = arreglaNombre(nombre)
            # Comprobar si existe ese nombre ya buscando en la bbdd
            records = db.session.query(Marca).filter_by(nombre=nombre).first()
            #Si no existe hará el update
            if(records == None):
                # Al objeto le cambiamos el atributo de nombre
                marca.nombre = nombre
                # Guardamos la sesssion de la bd
                db.session.commit()
                # mostramos mensaje de flask al html
                flash("Marca updateado satisfactoriamente!")
                # Función de redirección de flask al index
                return redirect(url_for('marcas.index'))
            else:
                flash("Error al hacer update elemento ya existe")
    return render_template('marcas/update.html', marca=marca)



