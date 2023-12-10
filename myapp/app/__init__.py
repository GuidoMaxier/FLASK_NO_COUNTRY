from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@localhost:3306/nombre_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app.routes import routesTasks  # Importa las rutas después de crear la aplicación Flask


if __name__ == "__main__":
    app.run(debug=True)


