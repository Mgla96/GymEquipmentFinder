from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
#db.init_app(app)

from app import routes


"""
def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    with app.app_context():
        from . import routes #routes
        db.create_all() #create sql tables for data models
        return app
"""
