import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import Bars, Plates, Dumbbells, Racks, Kettlebells

from time import sleep
import re
from requests import get 
from random import randint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
manager = Manager(app)

def randomWait():
    tm=randint(1,6)
    sleep(tm)

def formatPrice(price):
    price=price.replace("$","")
    price=price.replace("\n","")
    price=price.replace(" ","")
    return price

def removeOldProducts():
    #Barbell
    bb = db.session.query(Bars).filter(lambda x: (x.date() - datetime.utcnow()) > 2)
    for x in bb:
        db.session.delete(x)
        db.session.commit()
    
    #Plates
    p = db.session.query(Plates).filter(lambda x: (x.date() - datetime.utcnow()) > 2)
    for x in p:
        db.session.delete(x)
        db.session.commit()

    #Dumbbells
    db = db.session.query(Dumbbells).filter(lambda x: (x.date() - datetime.utcnow()) > 2)
    for x in db:
        db.session.delete(x)
        db.session.commit()
      
def Rogue():
    #Barbell
    response = get('https://www.roguefitness.com/weightlifting-bars-plates/barbells/mens-20kg-barbells?limit=80')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li',class_='item')
    for post in posts:
        search_header = post.find('div', class_='product-details')
        if not search_header:
            continue
        productName = search_header.find('h2',class_='product-name').text
        productLink = search_header.find('a').get('href')
        productPrice = search_header.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        page_container = html_soup2.find('div',class_='main-container')
        tmp = page_container.find('div',class_='add-to-cart')
        if tmp:
            tmp2 = tmp.find('button')
        else:
            tmp2 = False
        inStock="Out of Stock"
        if tmp2:
            if tmp2.text == "Add to Cart":
                inStock="In Stock"
        if productPrice:
            #if productPrice[0]=="$":
            #    productPrice=productPrice[1:]
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
        tmp3 = db.session.query(Bars).filter_by(name=productName).first()
        if tmp3:
            tmp3.stock=inStock 
            tmp3.price=productPrice 
        else:
            tmp4 = Bars(name=productName,brand="Rogue",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp4)
            except:
                print("exception occured rogue")
        db.session.commit()
        randomWait()
    
    #Plates
    response = get('https://www.roguefitness.com/weightlifting-bars-plates/bumpers?limit=80')
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
        tmp = page_container.find('div',class_='add-to-cart')
        if tmp:
            tmp2 = tmp.find('button')
        else:
            tmp2 = False
        inStock="Out of Stock"
        if tmp2:
            if tmp2.text == "Add to Cart":
                inStock="In Stock"
        if productPrice:
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
        tmp3 = db.session.query(Plates).filter_by(name=productName).first()
        if tmp3:
            tmp3.stock=inStock 
            tmp3.price=productPrice
        else:
            tmp4 = Plates(name=productName,brand="Rogue",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp4)
            except:
                print("exception occured rogue plate")
        db.session.commit()
        randomWait()
    '''
    #Rogue Kettlebells
    response = get('https://www.roguefitness.com/conditioning/strength-equipment/kettlebells?gclid=Cj0KCQjwsuP5BRCoARIsAPtX_wFq_3o7IKH_cRBzNgiGG-j2joxuDmEqrMjtmvwilehXiI0nNIgtvyEaArd8EALw_wcB?limit=80')
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

        grouped_items = page_container.find_all('div',class_="grouped-item")
    
        for group in grouped_items:
            item_name=group.find("div",class_="item-name").text
            if "Monster" in productName:
                item_name="Monster "+item_name
            item_price=group.find("span",class_="price").text
            item_price=formatPrice(item_price)
            if group.find("div",class_="item-qty input-text"):
                item_stock="In Stock"
            else:
                item_stock="Out of Stock"
            tmp3 = db.session.query(Kettlebells).filter_by(name=productName).first()
            if tmp3:
                tmp3.stock=item_stock 
                tmp3.price=item_price 
            else:
                tmp4 = Kettlebells(name=item_name,brand="Rogue",link=productLink[:160],price=item_price[:12],image="",stock=item_stock)
                try:
                    db.session.add(tmp4)
                except:
                    print("exception occured rogue")
            print("commit")
            db.session.commit()
        if not grouped_items:
            tmp = page_container.find('div',class_='add-to-cart')
            if tmp:
                tmp2 = tmp.find('button')
            else:
                tmp2 = False
            inStock="Out of Stock"
            if tmp2:
                if tmp2.text == "Add to Cart":
                    inStock="In Stock"
            if productPrice:
                test = productPrice.find("$")
                if test!=-1:
                    productPrice=productPrice[test+1:]
            
            tmp3 = db.session.query(Kettlebells).filter_by(name=productName).first()
            if tmp3:
                tmp3.stock=inStock 
                tmp3.price=productPrice 
            else:
                tmp4 = Kettlebells(name=productName,brand="Rogue",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                try:
                    db.session.add(tmp4)
                except:
                    print("exception occured rogue")
            print("commit")
            db.session.commit()
        randomWait()
    '''



def XMark():
    #Barbell ..
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
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            tmp2 = db.session.query(Bars).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
                tmp2.price=productPrice
            else:
                tmp = Bars(name=productName,brand="XMark",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured xmark")
            db.session.commit()
        randomWait()
    #Plates
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
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            tmp2 = db.session.query(Plates).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
                tmp2.price=productPrice
            else:
                tmp = Plates(name=productName,brand="XMark",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured xmark plates")
            db.session.commit() 
        randomWait()
    #Dumbbell
    response=get("https://www.xmarkfitness.com/free-weights/dumbbells/?limit=80")
    html_soup = BeautifulSoup(response.text, 'html.parser')
    dumbbells = html_soup.find_all('li',class_='Odd') #<li class="result-row">
    dumbbells2 = html_soup.find_all('li',class_='Even')
    dumbbells = dumbbells + dumbbells2
    for dumbbell in dumbbells:
        a=dumbbell.find("a",class_="pname")
        productName=a.text
        productLink=a.get("href")
        productPrice=dumbbell.find("em",class_="p-price").text
        outStock=dumbbell.find("a",class_="icon-Out")
        inStock=dumbbell.find("a",class_="icon-Add")
        if inStock:
            inStock="In Stock"
        elif outStock:
            inStock=outStock.text
        else:
            inStock="Out of stock"
        if productName:
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            tmp2 = db.session.query(Dumbbells).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock 
                tmp2.price=productPrice  
            else:
                tmp = Dumbbells(name=productName,brand="XMark",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured xmark dumbbell")
            db.session.commit()
        randomWait()

def REP():
    #REP Men's 20KG Barbell - should be good
    response = get('https://www.repfitness.com/bars-plates/olympic-bars')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bars = html_soup.find_all('li',class_='item')
    for bar in bars:
        prodInfo = bar.find('h2', class_='product-name')
        pricecont = bar.find('div', class_='price-container')
        if not prodInfo:
            continue
        productName = prodInfo.text[:100]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text
        if not inStock:
            inStock=""
        if productName:
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            tmp2 = db.session.query(Bars).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
                tmp2.price=productPrice
            else:
                tmp = Bars(name=productName,brand="REP",link=productLink[:160],price=productPrice[1:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    #REP Plates
    response = get('https://www.repfitness.com/catalogsearch/result/index/?cat=113&q=plates')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item') #<li class="result-row">
    for plate in plates:
        prodInfo = plate.find('h2', class_='product-name')
        pricecont = plate.find('div', class_='price-container')
        if not prodInfo:
            continue
        productName = prodInfo.text[:-2]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text[1::]
        productPrice = formatPrice(productPrice)
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text
        if not inStock:
            inStock=""
        if productName:
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            
            tmp2 = db.session.query(Plates).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock
                tmp2.price=productPrice
            else:
                tmp = Plates(name=productName,brand="REP",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    
    #REP dumbbell
    response = get('https://www.repfitness.com/conditioning/strength-equipment/dumbbells')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all('li',class_='item') #<li class="result-row">
    for plate in plates:
        prodInfo = plate.find('h2', class_='product-name')
        pricecont = plate.find('div', class_='price-container')
        if not prodInfo:
            continue
        productName = prodInfo.text[:-2]
        productLink = prodInfo.find('a').get('href')
        productPrice = pricecont.find('span',class_='price').text[1::]
        productPrice = formatPrice(productPrice)
        ownPage = get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        info = html_soup2.find('p',class_='availability')
        inStock = info.find('span').text
        if not inStock:
            inStock=""
        if productName:
            test = productPrice.find("$")
            if test!=-1:
                productPrice=productPrice[test+1:]
            tmp2 = db.session.query(Dumbbells).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock   
                tmp2.price=productPrice  
            else:
                tmp = Dumbbells(name=productName,brand="REP",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    
def Titan():
    #Weight Plates
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
                tmp2.price=productPrice
            else:
                tmp = Plates(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    #Barbells
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
                tmp2.price=productPrice
            else:
                tmp = Bars(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    #Dumbbells
    response = get('https://www.titan.fitness/strength/dumbbells/')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    dumbbells = html_soup.find_all('div',class_='product') #<li class="result-row">
    for dumbbell in dumbbells:
        tst = dumbbell.find('div',class_='image-container')
        prd = tst.find('img', class_='tile-image')
        productName = prd.get('title')
        productLink = 'https://www.titan.fitness/'+tst.find('a',class_='gtm-product-list').get('href')
        prod = dumbbell.find('span',class_='value')
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
            tmp2 = db.session.query(Dumbbells).filter_by(name=productName).first()
            if tmp2:
                tmp2.stock=inStock 
                tmp2.price=productPrice
            else:
                tmp = Dumbbells(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                try:
                    db.session.add(tmp)
                except:
                    print("exception occured")
            db.session.commit()
        randomWait()
    '''
    #Racks
    response = get('https://www.titan.fitness/racks/power-racks/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('div',class_='product') #<li class="result-row">
    for post in posts:
        tst = post.find('div',class_='image-container')
        prd = tst.find('img', class_='tile-image')
        productName = prd.get('title')
        if productName=="TITAN Series Power Rack":
            continue
        else:
            productLink = 'https://www.titan.fitness/'+tst.find('a',class_='gtm-product-list').get('href')
            prod = post.find('span',class_='value')
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
                        tmp = html_soup2.find('div',class_='attribute attribute-size')
                        inStock=html_soup2.find('span',class_='availability-msg').text
                        if inStock and "Select Styles for Availability" in inStock and tmp:
                            a = tmp.find_all('option',value='null')
                            b = tmp.find_all('option')
                            if (len(b)-len(a))>1:
                                inStock="In Stock"
                            else:
                                inStock="Out of Stock"
                else:
                    inStock = page_container.text
                tmp2 = db.session.query(Racks).filter_by(name=productName).first()
                if tmp2:
                    tmp2.stock=inStock 
                    tmp2.price=productPrice
                else:
                    tmp = Racks(name=productName,brand="Titan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock)
                    try:
                        db.session.add(tmp)
                    except:
                        print("exception occured")
                db.session.commit()
        randomWait()
    '''
       
        
def Fringe():
    #Plates 
    response = get('https://www.fringesport.com/collections/bumper-plates/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    plates = html_soup.find_all("div",class_="odd")
    plates2 = html_soup.find_all("div",class_="even")
    plates=plates+plates2
    for plate in plates:
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
            productPrice=formatPrice(productPrice)
        else:
            productPrice="-1"
        soldout=omega.find("span",class_="sold_out")
        if soldout:
            if "Sold Out" in soldout.text:
                inStock="Out of Stock"
            elif "Pre-Order" in soldout.text or "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        else:
            if "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        tmp2 = db.session.query(Plates).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            tmp2.price=productPrice
        else:
            tmp = Plates(name=productName,brand="Fringe Sport",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp)
            except:
                print("exception occured")
        #print(productName,"Fringe Sport",productLink[:160],inStock)
        db.session.commit()
        randomWait()
    #Barbells
    response = get('https://www.fringesport.com/collections/barbells/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bar = html_soup.find_all("div",class_="odd")
    bar2 = html_soup.find_all("div",class_="even")
    bars=bar+bar2
    for bar in bars:
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
            productPrice=formatPrice(productPrice)
        else:
            productPrice="None"
        soldout=omega.find("span",class_="sold_out")
        if soldout:
            if "Sold Out" in soldout.text:
                inStock="Out of Stock"
            elif "Pre-Order" in soldout.text or "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        else:
            if "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        tmp2 = db.session.query(Bars).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            tmp2.price=productPrice
            db.session.add(tmp2)
        else:
            tmp = Bars(name=productName,brand="Fringe Sport",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp)
            except:
                print("exception occured")
        db.session.commit()  
        randomWait()
     
def Vulcan():
    #Cast Iron Plates
    response = get('https://www.vulcanstrength.com/Vulcan-Cast-Iron-Olympic-Steel-Plates-p/v-ci-oly.htm?')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all("tr",class_="Multi-Child_Background")
    for post in posts: 
        prod = post.find('td',class_='colors_productname')
        if prod:
            productName=prod.text
        productPrice = post.find('span')
        if productPrice: #hard one
            if productPrice.text[0]=="$":
                productPrice=productPrice.text
        inStock = post.find('span',class_="in-stock")     
        if inStock:
            if "Out of Stock" in inStock.text:
                inStock = "Out of Stock"
            else:
                inStock = "In Stock"
        else:
            inStock="Out of Stock"
        
        productLink="https://www.vulcanstrength.com/Vulcan-Cast-Iron-Olympic-Steel-Plates-p/v-ci-oly.htm?"
        tmp2 = db.session.query(Plates).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            tmp2.price=productPrice
        else:
            tmp = Plates(name=productName,brand="Vulcan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp)
            except:
                print("exception occured")
        db.session.commit()  
        randomWait()

    #Bumper Plates
    response = get('https://www.vulcanstrength.com/Bumper-Plates-s/356.htm')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    tmp = html_soup.find('ul',class_="vnav--level3")
    posts = tmp.find_all('a',class_='vnav__link') 
    for post in posts:
        productLink = post.get('href')
        ownPage=get(productLink)
        html_soup2 = BeautifulSoup(ownPage.text, 'html.parser')
        posts2 = html_soup2.find_all("tr",class_="Multi-Child_Background")
        if len(posts2)>0:
            for post2 in posts2: 
                prod = post2.find('td',class_='colors_productname')
                if prod:
                    productName=prod.text
                productPrice = post2.find('span')
                if productPrice: 
                    productPrice=productPrice.text
                    if productPrice[0]=="$":
                        productPrice=productPrice[1:]
                
                inStock = post.find('span',class_="in-stock")     
                if inStock:
                    if "Out of Stock" in inStock.text:
                        inStock = "Out of Stock"
                    else:
                        inStock = "In Stock"
                else:
                    inStock="Out of Stock"
                tmp2 = db.session.query(Plates).filter_by(name=productName).first()
                if tmp2:
                    tmp2.stock=inStock
                    tmp2.price=productPrice
                else:
                    tmp = Plates(name=productName,brand="Vulcan",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
                    try:
                        db.session.add(tmp)
                    except:
                        print("exception occured")
                db.session.commit()  
        randomWait()


def Alt():
    #Barbells
    response = get('https://www.fringesport.com/collections/barbells/?size=90')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    bar = html_soup.find_all("div",class_="odd")
    bar2 = html_soup.find_all("div",class_="even")
    bars=bar+bar2
    for bar in bars:
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
            productPrice=formatPrice(productPrice)
        else:
            productPrice="None"
        soldout=omega.find("span",class_="sold_out")
        if soldout:
            if "Sold Out" in soldout.text:
                inStock="Out of Stock"
            elif "pre-order" in soldout.text.lower() or "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        else:
            if "order" in productName.lower():
                inStock="Backorder"
            else:
                inStock="In Stock"
        tmp2 = db.session.query(Bars).filter_by(name=productName).first()
        if tmp2:
            tmp2.stock=inStock
            tmp2.price=productPrice
        else:
            tmp = Bars(name=productName,brand="Fringe Sport",link=productLink[:160],price=productPrice[:12],image="",stock=inStock,date=datetime.utcnow())
            try:
                db.session.add(tmp)
            except:
                print("exception occured")
        db.session.commit()  
        randomWait()      

@manager.command
def hello():
    print("hello")
@manager.command
def scrpe():
    XMark()
    REP()
    Titan()    
@manager.command
def scrpe2():
    Rogue()
    Vulcan()
    Fringe()
@manager.command
def alt(): 
    Alt()

@manager.command
def updateXMark(): 
    XMark()
@manager.command
def updateREP(): 
    REP()
@manager.command
def updateTitan(): 
    Titan()
@manager.command
def updateRogue(): 
    Rogue()
@manager.command
def updateVulcan(): 
    Vulcan()
@manager.command
def updateFringe(): 
    Fringe()
@manager.command
def removeProducts(): 
    removeOldProducts()

if __name__ == '__main__':
    manager.run()

