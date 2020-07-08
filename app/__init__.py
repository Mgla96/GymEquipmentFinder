from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_talisman import Talisman
from config import Config

app = Flask(__name__)
#Talisman(app)
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
}
talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src']
)

app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
db.init_app(app)

from app import routes, models

