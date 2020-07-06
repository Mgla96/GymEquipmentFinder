from flask import render_template
from app import app
from .models import db, Bars, Plates

@app.route('/')
@app.route('/index')
def index():
    #plates,barbells = [],[]
    print("QUERY::::",Bars.query.all)
    user={
        'username':'Bill',
        'bars':Bars.query.all,
        'plates':Plates.query.all
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all,plates=Plates.query.all)


#python3 -m flask run
