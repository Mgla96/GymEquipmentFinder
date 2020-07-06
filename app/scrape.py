from bs4 import BeautifulSoup
from time import sleep
import re
from requests import get 
import numpy as np
from random import randint

from .models import db

#Rogue Mens 20kg Barbells

    
def scrpe():
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
        cmd = "INSERT INTO Bars (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        db.execute(cmd)
        db.commit()


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
        cmd = "INSERT INTO Plates (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        db.execute(cmd)
        db.commit()
  

    #REP Men's 20KG Barbell
    response = get('https://www.repfitness.com/bars-plates/olympic-bars')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bars = html_soup.find_all('li',class_='item')
    for bar in bars:
        prodInfo = bar.find('h2', class_='product-name')
        pricecont = bar.find('div', class_='price-container')
        productName = prodInfo.text
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text

        cmd = "INSERT INTO Bars (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        db.execute(cmd)
        db.commit()
    
    #REP Plates
    response = get('https://www.repfitness.com/catalogsearch/result/index/?cat=113&q=plates')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item') #<li class="result-row">
    for plate in plates:
        prodInfo = plate.find('h2', class_='product-name')
        pricecont = plate.find('div', class_='price-container')
        productName = prodInfo.text[:-2]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text
        cmd = "INSERT INTO Plates (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        db.execute(cmd)
        db.commit()

scrpe()