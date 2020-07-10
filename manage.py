import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import Bars, Plates

from time import sleep
import re
from requests import get 
from random import randint
from bs4 import BeautifulSoup

manager = Manager(app)

@manager.command
def hello():
    print("hello")
@manager.command
def scrpe():
    #XMark Barbell
    response = get('https://www.xmarkfitness.com/bars/?limit=80')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li',class_='Odd') #<li class="result-row">
    posts2 = html_soup.find_all('li',class_='Even')
    bars = posts + posts2
    for bar in bars:
        a=bar.find("a",class_="pname")
        productName=a.text
        productLink=a.get("href")
        productPrice=bar.find("em",class_="p-price").text
        outStock=bar.find("a",class_="icon-Out")
        inStock=bar.find("a",class_="icon-Add")
        if inStock:
            inStock="In Stock"
        elif outStock:
            inStock=outStock.text
        else:
            inStock="Out of stock"
        if productName:
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            tmp2 = db.session.query(Bars).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
            else:
                tmp = Bars(name=productName,brand="XMark",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                db.session.add(tmp)
            db.session.commit()

    #XMark Plates
    response = get('https://www.xmarkfitness.com/free-weights/weight-plates/?limit=80')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li',class_='Odd') #<li class="result-row">
    posts2 = html_soup.find_all('li',class_='Even')
    bars = posts + posts2
    for bar in bars:
        a=bar.find("a",class_="pname")
        productName=a.text
        productLink=a.get("href")
        productPrice=bar.find("em",class_="p-price").text
        outStock=bar.find("a",class_="icon-Out")
        inStock=bar.find("a",class_="icon-Add")
        if inStock:
            inStock="In Stock"
        elif outStock:
            inStock=outStock.text
        else:
            inStock="Out of stock"
        if productName:
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            tmp2 = db.session.query(Plates).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
            else:
                tmp = Plates(name=productName,brand="XMark",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                db.session.add(tmp)
            db.session.commit()   

    #REP Men's 20KG Barbell - should be good
    response = get('https://www.repfitness.com/bars-plates/olympic-bars')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bars = html_soup.find_all('li',class_='item')
    for bar in bars:
        prodInfo = bar.find('h2', class_='product-name')
        pricecont = bar.find('div', class_='price-container')
        productName = prodInfo.text[:100]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        stockbl = info.find('span').text
        if not stockbl:
            stockbl=""
        if productName:
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            tmp2 = db.session.query(Bars).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=stockbl
            else:
                tmp = Bars(name=productName,brand="REP",link=productLink[:160],price=productPrice[1:12],image="",stock=stockbl)
                db.session.add(tmp)
            db.session.commit()
    
    #REP Plates
    response = get('https://www.repfitness.com/catalogsearch/result/index/?cat=113&q=plates')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item') #<li class="result-row">
    for plate in plates:
        prodInfo = plate.find('h2', class_='product-name')
        pricecont = plate.find('div', class_='price-container')
        productName = prodInfo.text[:-2]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text[1::]
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text
        if not stockbl:
            stockbl=""
        if productName:
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            tmp2 = db.session.query(Plates).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=stockbl
            else:
                tmp = Plates(name=productName,brand="REP",link=productLink[:160],price=productPrice[:12],image="",stock=stockbl)
                db.session.add(tmp)
            db.session.commit()
    

    #titan
    response = get('https://www.titan.fitness/strength/weight-plates/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('div',class_='product') #<li class="result-row">
    for plate in plates:
        tst = plate.find('div',class_='image-container')
        prd = tst.find('img', class_='tile-image')
        productName = prd.get('title')
        #img = prd.get('src')
        productLink = 'https://www.titan.fitness/'+tst.find('a',class_='gtm-product-list').get('href')
        prod = plate.find('span',class_='value')
        if prod:
            productPrice=prod.get('content')
        else:
            productPrice="?"
        if productName and productPrice!="?":
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            ownPage = get(productLink)
            html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
            page_container = html_soup2.find('span',class_='strong')
            if not page_container:
                inStock = html_soup2.find('span',class_="in-stock")
                if inStock:
                    inStock=inStock.text
                    if inStock!="In Stock":
                        inStock="Out of Stock"
                else:
                    inStock="Out of Stock"
            else:
                inStock = page_container.text
            tmp2 = db.session.query(Plates).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
            else:
                tmp = Plates(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                db.session.add(tmp)
            db.session.commit()

    response = get('https://www.titan.fitness/strength/barbells/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bars = html_soup.find_all('div',class_='product') #<li class="result-row">
    for bar in bars:
        tst = bar.find('div',class_='image-container')
        prd = tst.find('img', class_='tile-image')
        productName = prd.get('title')
        productLink = 'https://www.titan.fitness/'+tst.find('a',class_='gtm-product-list').get('href')
        #img = prd.get('src')
        prod = bar.find('span',class_='value')
        if prod:
            productPrice=prod.get('content')
        else:
            productPrice="?"
        if productName and productPrice!="?":
            if productPrice[0]=="$":
                productPrice=productPrice[1:]
            ownPage = get(productLink)
            html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
            page_container = html_soup2.find('span',class_='strong')
            if not page_container:
                inStock = html_soup2.find('span',class_="in-stock")
                if inStock:
                    inStock=inStock.text
                    if inStock!="In Stock":
                        inStock="Out of Stock"
                else:
                    inStock="Out of Stock"
            else:
                inStock = page_container.text
            tmp2 = db.session.query(Bars).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
            else:
                tmp = Bars(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                db.session.add(tmp)
            db.session.commit()
@manager.command
def scrpe2():
    #Fringe Sport Plates
    response = get('https://www.fringesport.com/collections/bumper-plates/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all("div",class_="odd")
    plates2 = html_soup.find_all("div",class_="even")
    plates=plates+plates2

    for plate in plates:
        productName = plate.find("a").title
        productLink = "https://www.fringesport.com"+plate.find("a").get("href")
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        omega = html_soup2.find("div",class_="eight columns omega")
        productName=omega.find("h1",class_="product_name")
        if productName:
            productName=productName.text
        else:
            productName=""
        productPrice=omega.find("span",class_="current_price")
        if productPrice:
            productPrice=productPrice.text
            productPrice=productPrice.replace(" ","")
            productPrice=productPrice.replace("\n","")
            if productPrice:
                if productPrice[0]!="$":
                    productPrice="None"
                else:
                    productPrice=productPrice[1:]
            else:
                productPrice="None"
        else:
            productPrice="-1"
        soldout=omega.find("span",class_="sold_out")
        if soldout:
            if "Sold Out" in soldout.text:
                inStock="Out of Stock"
            else:
                inStock="In Stock"
        else:
            inStock="In Stock"
        tmp2 = db.session.query(Plates).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            db.session.commit()
            print(tmp2.stock)
        else:
            tmp = Plates(name=productName,brand="Fringe Sport",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
            db.session.add(tmp)
            db.session.commit()
     
    #Fringe Sport Barbells
    response = get('https://www.fringesport.com/collections/bumper-plates/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bar = html_soup.find_all("div",class_="odd")
    bar2 = html_soup.find_all("div",class_="even")
    bars=bar+bar2

    for bar in bars:
        productName = bar.find("a").title
        productLink = "https://www.fringesport.com"+bar.find("a").get("href")
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        omega = html_soup2.find("div",class_="eight columns omega")
        productName=omega.find("h1",class_="product_name")
        if productName:
            productName=productName.text
        else:
            productName=""
        productPrice=omega.find("span",class_="current_price")
        if productPrice:
            productPrice=productPrice.text
            productPrice=productPrice.replace(" ","")
            productPrice=productPrice.replace("\n","")
            if productPrice:
                if productPrice[0]!="$":
                    productPrice="None"
                else:
                    productPrice=productPrice[1:]
            else:
                productPrice="None"
        else:
            productPrice="-1"
        soldout=omega.find("span",class_="sold_out")
        if soldout:
            if "Sold Out" in soldout.text:
                inStock="Out of Stock"
            else:
                inStock="In Stock"
        else:
            inStock="In Stock"
        tmp2 = db.session.query(Bars).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            db.session.commit()
            print(tmp2.stock)
        else:
            tmp = Bars(name=productName,brand="Fringe Sport",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
            db.session.add(tmp)
            db.session.commit()   
    
#manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()