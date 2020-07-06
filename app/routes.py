from flask import render_template
from app import app
from .models import db, Bars, Plates

@app.route('/')
@app.route('/index')
def index():
    #plates,barbells = [],[]
    #print("QUERY::::",Bars.query.all)
    user={
        'username':'Bill',
        'bars':Bars.query.all,
        'plates':Plates.query.all
    }
    return render_template('index.html',title='Home',user=user,bars=Bars.query.all,plates=Plates.query.all)


#python3 -m flask run

"""
scratch

  {%for bar in bars%}
                <div class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-3">
                    <span class="field-name">Name: </span>
                    <span class="field-value">{{bar.name}}</span>
                    <span class="field-name">Price: </span>
                    <span class="field-value">{{bar.price}}</span>
                    <span class="field-value">{{bar.image}}</span>
                    <span class="field-name">Link: </span>
                    <span class="field-value">{{bar.link}}</span>
                    <span class="field-name">Available?: </span>
                    <span class="field-value">{{bar.stock}}</span>
                </div>
                {%endfor%}

                

{%for plate in plates%}
                    <div class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-3">
                        <span class="field-name">Name: </span>
                        <span class="field-value">{{plate.name}}</span>
                        <span class="field-name">Price: </span>
                        <span class="field-value">{{plate.price}}</span>
                        <span class="field-value">{{plate.image}}</span>
                        <span class="field-name">Link: </span>
                        <span class="field-value">{{plate.link}}</span>
                        <span class="field-name">Available?: </span>
                        <span class="field-value">{{plate.stock}}</span>
                    </div>
                    {%endfor%}






"""