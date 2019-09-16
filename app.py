from flask import Flask, render_template, request, redirect, url_for, jsonify
from bs4 import BeautifulSoup,Tag
from flask_celery import make_celery 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scripts import * 
import subprocess, json

#subprocess.call(["python", "/home/pi/Projects/Garbage_Detector/webapp/scripts/introScript.py"], shell=False)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

#This is used to set up the message broker
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
#This is to add the database for Celery to store its results into.
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = make_celery(app)

def refreshList():
    with open("./templates/frontPage.html") as fp:
        soup = BeautifulSoup(fp)
    body = soup.find('body')
    aliveLists = soup.find('ol')
    listTags = soup.new_tag('ol')
    listOfEmails=["a","b","c"]
    i = 0
    for x in listOfEmails:
        listTags.insert(i,listOfEmails[i])
        ++i
    if str(aliveLists) != "None":
        print("Found an ol")
        soup.find('ol').decompose()

    body.insert(1, listTags)

    with open("./templates/frontPage.html", "w") as outf:
        outf.write(str(soup))   
    return

#Tip: Every function's name must be the same as that of the html file
@app.route('/hello/<n>')
def hello(n):
    reverse.delay(n)
    return 'sent async request'
    #return render_template('page.html', name=n)

@celery.task(name='celery example')
def reverse(string):
    return string[::-1]

@app.route('/dataPage')
def dataPage():
    return render_template('dataPage.html')

@app.route('/inputEmail', methods=['POST'])
def inputEmail():
    return render_template('inputEmail.html')

#The 'GET' indicates that the html form will return a query string version of 
#the input while the 'POST' indicates that the html form will return form data
#Query strings are strings that are typically saved in databases and for searches
#Form data is essentially raw data.
@app.route('/processInput', methods=['GET', 'POST'])
def processInput():
    index = 1
    x = request.form['EmailInput']
    print("The input is " + x)
    return redirect(url_for('frontPage'))#, users=users))

@app.route('/processRemoval', methods=['GET', 'POST'])
def processRemoval():
    return redirect(url_for('frontPage'))

@app.route('/', methods=['GET', 'POST'])
def frontPage():
    refreshList()
    return render_template('parent.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
