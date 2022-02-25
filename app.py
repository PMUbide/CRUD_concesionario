# Importar el framework
from flask import Flask

# Se crea para instanciar la bbdd
from flask_sqlalchemy import SQLAlchemy

# Configuración básica para el servidor, inicializar en la variable app. Que es en sí la app servidor
app = Flask(__name__)

# Para pasarle la configuración que necesitará la base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/concesionario.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Recibe la app, y se instnacia como una bd
db = SQLAlchemy(app)
