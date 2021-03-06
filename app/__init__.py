from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_compress import Compress
from config import Config

app = Flask(__name__)
Compress(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
db.init_app(app)

from app import routes, models

