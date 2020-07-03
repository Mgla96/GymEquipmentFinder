from flask import render_template
from app import app
from bs4 import BeautifulSoup

#from .models import db, Bars, Plates

@app.route('/')
@app.route('/index')
def index():
    class Product:
        def __init__(self,name,price,link,availability):
            self.name = name
            self.price = price
            self.link = link
            self.availability = availability
            self.image = ""
    #plates,barbells = [],[]
    user={
        'username':'Bill'
    }
    #return render_template('index.html',title='Home',user=user,barbells=Barbells.query.all,plates=Plates.query.all)
    return render_template('index.html',title='Home',user=user)


#python3 -m flask run
