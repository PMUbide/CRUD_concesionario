# Importar el framework
from flask import Flask, render_template
# Se crea para instanciar la bbdd
from flask_sqlalchemy import SQLAlchemy
# Se importan los service
from routes.serie import series
from routes.marca import marcas
from routes.vehiculo import vehiculos

# Configuración básica para el servidor, inicializar en la variable app. Que es en sí la app servidor
app = Flask(__name__)

# Para pasarle la configuración que necesitará la base
app.secret_key = 'secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/concesionario.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Recibe la app, y se instancia como una bd
db = SQLAlchemy(app)

# Función para lanzar el template de error 404 en caso de suceder en el servidor
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Se registra en el objeto de la configuración los blueprints creados en los services en routes/
app.register_blueprint(series)
app.register_blueprint(marcas)
app.register_blueprint(vehiculos)
# Función para registrar la página de error
app.register_error_handler(404, page_not_found)

