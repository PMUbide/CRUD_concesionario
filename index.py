from app import app
from utils.db import db
import os

# cuando arranque la app creará el modelo definido
with app.app_context():
    db.create_all()


# Condición para verififcar si se ejecuta como proyecto principal
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(debug=True, host='0.0.0.0', port=port)
    app.run(debug=True)