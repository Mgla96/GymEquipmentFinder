#python3 -m flask run

from flask import render_template

from app import app
#import pandas as pd
import numpy as np
from random import randint
from time import sleep
import re
from requests import get 
from bs4 import BeautifulSoup

from .models import db, Bars, Plates

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
    plates,barbells = [],[]

    '''
    #Rogue Mens 20kg Barbells
    response = get('https://www.roguefitness.com/weightlifting-bars-plates/barbells/mens-20kg-barbells?limit=80')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li',class_='item') 
    for post in posts:
        search_header = post.find('div', class_='product-details')
        productName = search_header.find('h2',class_='product-name').text
        productLink = search_header.find('a').get('href')
        productPrice = search_header.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        page_container = html_soup2.find('div',class_='main-container')
        avail = page_container.find('div',class_='bin-stock-availability')
        inStock=True
        if avail.find('div',class_='bin-signup-dropper'):
            inStock=False
        else:
            inStock=True
        print(productName)
        print(productLink)
        print("Price:",productPrice)
        print("In Stock?: ",inStock,"\n")
    #Rogue Plates
    response = get('https://www.roguefitness.com/weightlifting-bars-plates/bumpers')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item')

    for plate in plates:
        search_header = plate.find('div', class_='product-details')
        productName = search_header.find('h2',class_='product-name').text
        productLink = search_header.find('a').get('href')     
        productPrice = search_header.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        page_container = html_soup2.find('div',class_='main-container')
        avail = page_container.find('div',class_='bin-stock-availability')
        inStock=True
        if avail.find('div',class_='bin-signup-dropper'):
            inStock=False
        else:
            inStock=True

        print(productName)
        print(productLink)
        print("Price:",productPrice)
        print("In Stock?: ",inStock)
    
    #REP Men's 20KG Barbell
    response = get('https://www.repfitness.com/bars-plates/olympic-bars')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bars = html_soup.find_all('li',class_='item')

    for bar in bars:
        prodInfo = bar.find('h2', class_='product-name')
        pricecont = bar.find('div', class_='price-container')
        name = prodInfo.text
        link = prodInfo.find('a').get('href')
        price = pricecont.find('span',class_='price').text
        ownPage = get(link)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        stock = info.find('span').text
        print(name)
        print(link)
        print("Price:",price)
        print(stock,"\n")
    
    #REP Plates
    response = get('https://www.repfitness.com/catalogsearch/result/index/?cat=113&q=plates')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item') #<li class="result-row">
    for plate in plates:
        prodInfo = plate.find('h2', class_='product-name')
        pricecont = plate.find('div', class_='price-container')
        name = prodInfo.text
        link = prodInfo.find('a').get('href')
        price = pricecont.find('span',class_='price').text
        ownPage = get(link)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        stock = info.find('span').text
        print(name[:-2])
        print(link)
        print("Price:",price)
        print(stock,"\n")
        print("-----------------")
    '''
    '''
    barbells.append("hello")
    barbells.append("test")
    plates.append("testplate")
    plates.append("testplate2")
    user={
        'username':'Bill',
        'barbells':barbells,
        'plates':plates
    }
    '''
    user={
        'username':'Bill'
    }

    return render_template('index.html',title='Home',user=user,barbells=Barbells.query.all,plates=Plates.query.all)
    