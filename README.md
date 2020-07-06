### Gym Equipment Finder
Tool to show weights and gym equipment that are in stock from popular brands

# Creating Venv

# Running
'''bash
python3 -m flask run
'''

# Activate Existing Venv





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
