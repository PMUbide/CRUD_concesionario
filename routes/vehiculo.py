#Imports de flask y componentes necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.serie import Serie
from models.vehiculo import Vehiculo
from utils.db import db

# Linea enroutador. Para llamarlo desde otras clases
vehiculos = Blueprint("vehiculos", __name__)

# Método que devuelve la vista de la lista de vehiculos 
@vehiculos.route("/vehiculos/")
def index():
    # Guarda el total de elementos en una variable de lista, y la lleva al template
    series = Serie.query.all()
    vehiculos = Vehiculo.query.all()
    return render_template("vehiculos/index.html", series=series, vehiculos= vehiculos)

# Método que se ejecuta cuando se guarda una nuevo vehiculo en la bbdd
@vehiculos.route("/vehiculos/new", methods=["POST"])
def add():
    # Con la función request de flask saca el valor  del form del template
    matricula = request.form["matricula"]
    color = request.form["color"]
    serie_id = request.form["serie_id"]
    # Comprobar si existe ese registro SOLO POR MATRICULA
    records = db.session.query(Vehiculo).filter_by(matricula=matricula).first()
    # Si no encuentra ninguno lo creará
    if records == None:
        # Comprobar si no está vacía la matricula
        if(matricula != ""):
            # Nuevo objeto para guardar
            new_vehiculo = Vehiculo(matricula, color)
            # añadirle a la serie el vehiculo que se ha creado   
            serie = Serie.query.get(serie_id)
            serie.vehiculos.append(new_vehiculo)
            # guardar el vehiculo en la bbdd
            db.session.add(new_vehiculo)
            # Ahora se acaba con la conexión y se hace commit
            db.session.commit()
            # Antes de reenviar, guardamos algo en la funcion flash
            flash("Vehículo añadido satisfactoriamente!")
            # Función de flask para hacer redirecciones 
            return redirect(url_for('vehiculos.index'))
        # Si está vacío no muestra mensaje y vuelve al index sin hacer nada
        return redirect(url_for('vehiculos.index')) 
    # Si ya existe indica el mensaje y vuele al index
    flash("Ese elemento ya existe")
    return redirect(url_for('vehiculos.index'))    


# Método que se acciona al escribir algo en el campo de búsqueda por matrícula de la vista
# Buscará ese elemento y devolverá como lista y si no devolverá uno vacío.
@vehiculos.route("/vehiculos/busqueda_matricula", methods=["POST"])
def search_matricula():
    # Recogemos la variable de matricula
    matricula2 = request.form["matricula2"]
    # Si no ha introducido nada en la búsqueda devuelve el index con todos vehiculos
    if matricula2 == '' :
        return redirect(url_for('vehiculos.index'))
    # Busqueda de elementos por la matricula.
    records = db.session.query(Vehiculo).filter_by(matricula=matricula2).first()
    #Cargamos todas las series también porque se necesita enviarse a la vista debido al formulario de creación y de busqueda por serie
    series = Serie.query.all()
    # Array para enviar según los resultados de "records"
    results = []
    # Si no está vacío lo añadirá al array. (Será de un sólo elemento siempre)
    if records != None:
        results.append(records)
    # Creamos una lista que siempre contiene todos los vehículos para el autocompletar de la vista
    vehiculos_total = Vehiculo.query.all()
    # Devuelve la vista del index con los vehiculos como el array results. Si está vacio pq no ha encontrado nada
    # lo gestionará la vista con un mensaje.
    return render_template("vehiculos/index.html", series=series, vehiculos= results, vehiculos_total=vehiculos_total)


# Método que se acciona al seleccionar algo en el campo de búsqueda por serie de la vista
# Buscará los registros que pertenezcan a esa serie y devolverá como lista.
@vehiculos.route("/vehiculos/busqueda_serie", methods=["POST"])
def search_serie():
    # Recogemos el objeto que coindice con el introducido del campo búsqueda
    serie_busqueda = request.form["serie_busqueda"]
    # Si no ha introducido nada en la búsqueda devuelve el index
    if serie_busqueda == 'None':
        return redirect(url_for('vehiculos.index'))
    # Busca los elementos que tengan esa serie_id
    records = db.session.query(Vehiculo).filter_by(serie_id=serie_busqueda).all()
    # Recogemos todas las series que hacen falta en la vista
    series = Serie.query.all()
    # Creamos una lista que siempre contiene todos los vehículos para el autocompletar de la vista
    vehiculos_total = Vehiculo.query.all()
    # Devuelve los vehiculos para el index con los que haya encontrado.
    return render_template("vehiculos/index.html", series=series, vehiculos= records, vehiculos_total=vehiculos_total)


# Función para eliminar un registro. Espera un id para hacer el delete
# Puede ser GET la primera vez que se ejecute para ir a la vista de confirmación de delete,
# Si se le da a SI en la vista de confirmación, entrará como método POST
@vehiculos.route("/vehiculos/delete/<id>", methods=["POST", "GET"])
def delete(id):
    # Guardamos el objeto que tenga ese id
    vehiculo = Vehiculo.query.get(id)
    # Si entra como método post
    if request.method == 'POST':
        # Se hace función eliminar de la bbdd de sqlalchemy
        db.session.delete(vehiculo)
        # Se guardan los cambios con commit de la bdd
        db.session.commit()
        # Devuelve mensaje a la vista y carga el index
        flash("Vehiculo borrado satisfactoriamente!")
        return redirect(url_for('vehiculos.index'))
    # Si entra como método GET devuelve la vista de confirmación de delete.
    return render_template('vehiculos/delete.html', vehiculo=vehiculo)


# Método para hacer un update de un elemento.
# Acepta los métodos de GET para llevar a la viste del update con el objeto,
# También el método POST cuando se haya ejecutado la opción de update del formulario.
@vehiculos.route("/vehiculos/update/<id>", methods=["POST", "GET"])
def update(id):
    #Guardamos en un objeto vehiculo con el id recibido
    vehiculo = Vehiculo.query.get(id)
    # Recogemos todas las series para mostrarla en la vista del update
    series = Serie.query.all()
    # Si entra como POST
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
            # Comprobar si existe ese registro POR MATRICULA por si cambia
            records = db.session.query(Vehiculo).filter_by(matricula=matricula).first()
            # Si no existe ese registro o si que existe pero es el mismo que el del objeto
            # pasará a ejecutar el update
            if(records == None or records.id == int(id)):
                # Cambiamos los valores al objeto
                vehiculo.matricula = matricula
                vehiculo.color = color
                vehiculo.serie_id = int(serie_id)
                # Commit para guardar la bbdd
                db.session.commit()
                # mensaje a la vista con el elemento flash de flask
                flash("Vehiculo updateado satisfactoriamente!")
                # Devuelve la vista de index de nuevo 
                return redirect(url_for('vehiculos.index'))
            # si si existe lo muestra y sigue en la pantalla de update    
            flash("Ese elemento ya existe!")    
    # si entra como GET devuelve la vista con el update y el objeto 
    return render_template('vehiculos/update.html', series=series, vehiculo=vehiculo)