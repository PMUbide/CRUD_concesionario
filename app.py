# Importar el framework
from flask import Flask

# Se crea para instanciar la bbdd
from flask_sqlalchemy import SQLAlchemy

from routes.serie import series
from routes.marca import marcas
from routes.vehiculo import vehiculos

# Configuración básica para el servidor, inicializar en la variable app. Que es en sí la app servidor
app = Flask(__name__)

app.secret_key = 'secret key'
# Para pasarle la configuración que necesitará la base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/concesionario.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Recibe la app, y se instnacia como una bd
db = SQLAlchemy(app)


app.register_blueprint(series)
app.register_blueprint(marcas)
app.register_blueprint(vehiculos)