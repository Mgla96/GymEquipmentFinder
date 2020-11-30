# Gym Equipment Finder
Due to COVID-19, available fitness equipment was very scarce and time-consuming to find. This application was created to solve that problem and display all in-stock items from numerous popular fitness brands on one page to save people time in their search.

### Demo Videos
See demo.mp4 for a demonstration of what this web application looked like when it was running.

### Creating Venv

### Activate Existing Venv
```bash
source venv/bin/activate
```

### Installing dependencies in Venv
```bash
pip3 install -r requirements.txt
```
or if python3 linked to pip
```bash
pip install -r requirements.txt
```

### Saving dependencies in requirements.txt
```bash
pip3 freeze > requirements.txt
```

### Seeing Custom Domains
```bash
heroku domains -a findweights
```

### Running
```bash
python3 -m flask run
```

### Establish psql session with your remote database
```bash
heroku pg:psql -a findweights
or
heroku pg:psql HEROKU_POSTGRESQL_JADE_URL -a findweights
```

### Querying Database from terminal
```bash
SELECT * FROM "Bars";
SELECT * FROM "Plates";
```

### Testing Scheduler 
```bash
heroku run python3 manage.py scrpe -a findweights
```
```bash
heroku run python3 manage.py scrpe2 -a findweights
```

### Commands to Directly use in Scheduler
```bash
python manage.py scrpe
```
```bash
python manage.py scrpe2
```

### Viewing Scheduler Logs
```bash
heroku logs --ps scheduler -a findweights
```