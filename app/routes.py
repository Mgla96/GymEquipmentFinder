from flask import render_template
from app import app
from .models import db, Bars, Plates

@app.route('/')
@app.route('/index')
def index():
    #plates,barbells = [],[]
    user={
        'username':'Bill',
        'bars':Bars.query.all,
        'plates':Plates.query.all
    }
    return render_template('index.html',title='Home',user=user)


#python3 -m flask run
