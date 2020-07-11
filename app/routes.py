from flask import render_template
from app import app
from .models import db, Bars, Plates, Racks, Dumbbells

from flask_script import Manager
manager = Manager(app)

@manager.command
def scrape2():
    print("hello")

@app.route('/')
@app.route('/index')
def index():
    db.create_all()
    user={
        'username':'Bill'
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all(),plates=Plates.query.all(),racks=Racks.query.all(),dumbbells=Dumbbells.query.all())

