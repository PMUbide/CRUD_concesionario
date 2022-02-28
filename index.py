from app import app
from utils.db import db

# cuando arranque la app creará el modelo definido
with app.app_context():
    db.create_all()


# Condición para verififcar si se ejecuta como proyecto principal
if __name__ == "__main__":
    app.run(debug=True)