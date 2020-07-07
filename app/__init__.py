from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
db.init_app(app)

from app import routes, models

