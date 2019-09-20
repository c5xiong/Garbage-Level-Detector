from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from collections import namedtuple
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from bs4 import BeautifulSoup,Tag
from flask_celery import make_celery 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scripts import * 
import subprocess, json, time
from werkzeug.urls import url_parse
from celery.schedules import crontab

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#import routes

login = LoginManager(app)

#This is used to set up the message broker
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
#This is to add the database for Celery to store its results into.
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = make_celery(app)

scheduleOfEmails = []
Person = namedtuple("Person", "email start finish")
FutureTime = namedtuple("FutureTime", "year month day")
calendar = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31,
            "6": 30, "7": 31, "8": 31, "9": 30, "10": 31, "11":
            30, "12": 31}
totalPeople=0

import models
from form import LoginForm, RegistrationForm

#Flask-Login always keeps track of the logged in user by storing the login's unique
#identifier in Flask's user session which is a storage space that is assigned 
#to each connected user. In short, whenever a user logs into the application, Flask
#will retrive its id from this storage and load into memory. The loader is register
# with @login.user_loader
@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Post': models.Post}

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('logIn'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('frontPage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('logIn'))
    return render_template('register.html', title='Register', form=form) 
        

@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    #The current_user variable comes from Flask_Login
    #This if statement is designed to redirect user to home pg if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('logIn'))
        login_user(user, remember=form.remember_me.data)
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        print("Logged into website")
        next_page = url_for('frontPage')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

login.login_view = 'logIn'
def refreshList():
    global totalPeople
    with open("./templates/frontPage.html") as fp:
        soup = BeautifulSoup(fp)
    body = soup.find('body')
    aliveLists = soup.find('ol')
    htmlList= "<ol>{0}<ol>"

    queryEmails = current_user.listOfEmails.all()
    totalEmails=[]
    index = 0
    for a in queryEmails:
        totalEmails.append(a.email)

        curtime = time.localtime(time.time())

        day =curtime.tm_mday + 7
        year = curtime.tm_year
        month = curtime.tm_mon

        if(day > calendar[str(month)]):
            day = (calendar[str(month)] + day) - calendar[str(month)]
            month+=1
            if(month == 13):
                month = month % 12
                year+=1
                
        futureTime = FutureTime(year = year, month = month, day = day)
        person = Person(email=a.email, start = curtime, finish = futureTime)
        scheduleOfEmails.append(a.email)
        ++index

    #If the numbers of emails changed, restart celery task
    if totalPeople != index:
        totalPeople = index
        celery.purge()
        runHardware.delay()
    liFormat= "<li>{0}</li>"
    liFormedList = [liFormat.format(a) for a in totalEmails]
    htmlList = htmlList.format("".join(liFormedList))

    i = 0
    if str(aliveLists) != "None":
        soup.find('ol').decompose()

    listTags = soup.new_tag('ol')
    for x in totalEmails:
        itemTags = soup.new_tag('li')
        itemTags.string = x
        listTags.insert(i, itemTags)
        ++i;

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

@celery.task(name="Run Arduino")
def runHardware():
    
    if scheduleOfEmails == []:
        refreshList()
    num = totalPeople
    for email in scheduleOfEmails:
        runArduino(email, --num)
    scheduleOfEmails = []
    return
    
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(runHardware(), name='add every 10')

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
    u = models.User.query.get(current_user.id)
    print(u)
    addition = models.Post(email=x, author=u, id=x)
    current_db_sessions=db.session.object_session(addition)
    current_db_sessions.add(addition)
    current_db_sessions.commit()

    return redirect(url_for('frontPage'))

@app.route('/removeEmail', methods=['GET', 'POST'])
def removeEmail():
    x = request.form['EmailRemoval']
    u = models.Post.query.all()
    for p in u:
        if(p.id == x):
            current_db_sessions=db.session.object_session(p)
            current_db_sessions.delete(p)
            break
    refreshList()
    return redirect(url_for('frontPage'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        refreshList()
        return render_template('parent.html')
    else:
        return render_template('logIn')

@app.route('/frontPage', methods=['GET', 'POST'])
def frontPage():
    totalPeople = 0
    if current_user.is_authenticated:
        refreshList()
        return render_template('parent.html')
    else:
        return render_template('logIn.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0')
