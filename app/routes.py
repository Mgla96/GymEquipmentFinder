from flask import render_template
from app import app
from .models import db, Bars, Plates


from bs4 import BeautifulSoup
from time import sleep
import re
from requests import get 
import numpy as np
from random import randint

@app.route('/')
@app.route('/index')
    
def index():
    db.create_all()
    user={
        'username':'Bill'
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all,plates=Plates.query.all)

