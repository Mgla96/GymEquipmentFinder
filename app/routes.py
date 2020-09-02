from flask import render_template, send_from_directory, request, make_response, redirect
from app import app
from .models import db, Bars, Plates, Racks, Dumbbells,Kettlebells
from flask_script import Manager
from urllib.parse import urlparse, urlunparse

manager = Manager(app)

@app.before_request
def before_request():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'weightsinstock.com':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.weightsinstock.com'
        return redirect(urlunparse(urlparts_list), code=301)
    if request.url.startswith('http://'):
        url=request.url.replace('http://','https://',1)
        code=301
        return redirect(url,code=code)
     
@app.route('/')
@app.route('/index')
def index():
    db.create_all()
    return render_template('index.html',title='Home',bars=Bars.query.all(),plates=Plates.query.all(),dumbbells=Dumbbells.query.all(),racks=Racks.query.all(),kettlebells=Kettlebells.query.all())

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/ads.txt')
def ads_txt():
    return app.send_static_file("ads.txt")

