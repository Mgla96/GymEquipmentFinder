### Gym Equipment Finder
Tool to show weights and gym equipment that are in stock from popular brands

# Creating Venv

# Activate Existing Venv
```bash
source venv/bin/activate
```
ex: if you get error no module psycopg2 it's because I forgot to do this

# Installing dependencies in Venv
```bash
pip3 install -r requirements.txt
```
or if python3 linked to pip
```bash
pip install -r requirements.txt
```

# Saving dependencies in requirements.txt ?
```bash
pip3 freeze > requirements.txt
```

# Seeing Custom Domains
```bash
heroku domains -a findweights
```

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

# Testing Scheduler 
Split into two scripts since the scraping takes long
```bash
heroku run python3 manage.py scrpe -a findweights
```
```bash
heroku run python3 manage.py scrpe2 -a findweights
```
```bash
heroku run python3 manage.py alt -a findweights
```

# Commands to Directly use in Scheduler
```bash
python manage.py scrpe
```
```bash
python manage.py scrpe2
```

# Viewing Scheduler Logs
```bash
heroku logs --ps scheduler -a findweights
```