# Easy Condo
Condominium Management System - CSIS Project

## How to Run Web Server
* Install [Python 3](https://www.python.org/downloads/)
* Create a python Virtual env `python3 -m venv easycondo-venv`
* Activate venv it
  * macOS/Linux `source easycondo-venv/bin/activate`
  * Windows `easycondo-venv\Scripts\activate.bat`
* Install dependencies `pip install -r requirements.txt`
* Run server `python manage.py runserver`
* run the script to populate database run on terminal `source scripts.sh`

### Importing Data to DB
   `python manage.py  loaddata db.json`


### Creating super user

`python manage.py createsuperuser`

### App Deployed and Running on Heroku
[Easy Condo ](https://easycondapp.herokuapp.com/)

### Extras Solving Problems
* Problems Related to Database - Reset Database
  * Delete `db.sqlite3`
  * Delete `migrations` folder
  * make migrations of Project `python manage.py makemigrations`
  * make migrations of the app `python manage.py makemigrations webapp`
  * migrate `python manage.py migrate`
  * Export db data `python manage.py dumpdata > db.json`


