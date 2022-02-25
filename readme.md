<https://www.youtube.com/watch?v=BP3D03CYFHA&ab_channel=FaztCode>

# Crear entorno virtual
Instalar para crear entornovistuales -> `pip install virtualenv`

Despues con python crear el entorno-> `py -m venv .venv`
En la terminal de VSC tiene que aparecer el entorno virtual. (Se puede configurar en VSC: "tecla F1", "Python: Select Interpreter", elegir el de .venv)
En VSC usar el mismo formatter en el proyecto: File -> Preferences -> Settings -> Extensions -> Ptython y Formatting: Provider = black

# Instalar módulo FLASK
Instalar los módulos necesarios 
`pip install flask`
`pip install Flask-SQLAlchemy`

o utilizar comando para que instale lo necesario: 
`pip install -r requirements.txt`



# Configurar proyecto

_ESTRUCTURA - Dividir archivo principal en carpetas_

La ventaja de Flask es que te crea el sólo el servicio de apache,etc. Y te despliega para verlo en el navegador.
Para evitar tener que cancelar el servidor y volver a levantar con los cambios se añade:
`app.run(debug=True)`

- Crear carpeta models, routes, templates y utils. En utils conexión a la bbdd con SQL ALchemy, nuestro orquestador ORM.

- Archivo **app.py** tendrá la configuración de la aplicación, y el **index.app** ejecutará el servicio

- Generar los enrutamientos para los conactos. (Get y POST, sin PUT y DELETE porque haría falta typescript.)

## Crear modelo BBDD
Importar flask-sqlalchemy, módulo que añade sqlAlchemy a la app de Flask: `pip install Flask-SQLAlchemy`
En **utils** generar la clase **db.py**, en models está la clase para generar la tabla de la bbdd. Cuando arranque la app se ejecutará las tablas.
