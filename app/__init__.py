from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from app import routes

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    with app.app_context():
        from . import routes #routes
        db.create_all() #create sql tables for data models
        return app

