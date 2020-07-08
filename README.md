### Gym Equipment Finder
Tool to show weights and gym equipment that are in stock from popular brands

# Creating Venv

# Activate Existing Venv
```bash
source venv/bin/activate
```
ex: if you get error no module psycopg2 it's because I forgot to do this
# Running
```bash
python3 -m flask run
```

# Establish psql session with your remote database
```bash
heroku pg:psql -a findweights
or
heroku pg:psql HEROKU_POSTGRESQL_JADE_URL -a findweights
```

# Querying Database from terminal
```bash
SELECT * from "Bars";
SELECT * from "Plates";
```


       #cmd = "INSERT INTO Plates (name, link, price, image, stock) VALUES (productName, productLink, productPrice, "", inStock) ON CONFLICT (id) DO UPDATE SET stock = excluded.stock, price = excluded.price)"
        #db.add(cmd)
        #db.commit()

                #cmd = "INSERT INTO Bars (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        #db.add(cmd)
        #db.commit()

              #cmd = "INSERT INTO Plates (name, link, price, image, stock) "+"VALUES (productName, productLink, productPrice, "", inStock) "+ "ON CONFLICT (id) DO UPDATE "+"SET stock = excluded.stock, "+"price = excluded.price)"
        #db.add(cmd)
        #db.commit()

             #cmd = "INSERT INTO Bars (name, link, price, image, stock) VALUES (productName, productLink, productPrice, "", inStock) ON CONFLICT (id) DO UPDATE SET stock = excluded.stock, price = excluded.price)"
        #db.add(cmd)
        #db.commit()