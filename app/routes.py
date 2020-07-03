#python3 -m flask run

from flask import render_template

from app import app
import numpy as np
from random import randint
from time import sleep
import re
from requests import get 
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