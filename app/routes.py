#python3 -m flask run

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user={'username':'Bill'}
    return render_template('index.html',title='Home',user=user)