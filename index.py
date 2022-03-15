# Se importa el objeto app de la clase creada con la configuración
from app import app
# Se importa el objeto con la base de datos
from utils.db import db
import os

# cuando arranque la app creará el modelo definido
with app.app_context():
    db.create_all()

# Condición para verififcar si se ejecuta como proyecto principal
if __name__ == "__main__":
    # DESCOMENTAR para cambiar el puerto y host por defecto
    # port = int(os.environ.get('PORT', 5000))
    # app.run(debug=True, host='0.0.0.0', port=port)
    # Arranca la aplicación
    app.run(debug=True)