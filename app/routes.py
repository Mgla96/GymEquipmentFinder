from flask import render_template, send_from_directory, request, make_response
from app import app
from .models import db, Bars, Plates, Racks, Dumbbells

from flask_script import Manager
manager = Manager(app)

@app.route('/')
@app.route('/index')
def index():
    db.create_all()
    user={
        'username':'Bill'
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all(),plates=Plates.query.all(),dumbbells=Dumbbells.query.all(),racks=Racks.query.all())

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
