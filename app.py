from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from bs4 import BeautifulSoup,Tag
from flask_celery import make_celery 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from scripts import * 
import subprocess, json
from flask import request
from werkzeug.urls import url_parse

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


import models
from form import LoginForm, RegistrationForm

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Post': models.Post}

@login.user_loader
def load_user(user_id):
    return None

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
        return redirect(url_for('/'))
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
    with open("./templates/frontPage.html") as fp:
        soup = BeautifulSoup(fp)
    body = soup.find('body')
    aliveLists = soup.find('ol')
    htmlList= "<ol>{0}<ol>"
    listOfEmails=["a","b","c"]
    liFormat= "<li>{0}</li>"
    liFormedList = [liFormat.format(a) for a in listOfEmails]
    htmlList = htmlList.format("".join(liFormedList))
    print(liFormedList)
    print(htmlList)

    i = 0
    if str(aliveLists) != "None":
        print("Found an ol")
        soup.find('ol').decompose()

    listTags = soup.new_tag('ol')
    for x in listOfEmails:
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
    return redirect(url_for('frontPage'))

@app.route('/removeEmail', methods=['GET', 'POST'])
def removeEmail():
    refreshList()
    return redirect(url_for('frontPage'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    refreshList()
    return render_template('parent.html')

@app.route('/frontPage', methods=['GET', 'POST'])
def frontPage():
    refreshList()
    return render_template('parent.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0')
