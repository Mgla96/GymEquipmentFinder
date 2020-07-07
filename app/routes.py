from flask import render_template
from app import app
from .models import db, Bars, Plates

@app.route('/')
@app.route('/index')
def index():
    db.create_all()
    scrpe2()
    user={
        'username':'Bill'
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all(),plates=Plates.query.all())

