from flask import Flask, render_template
from flask_celery import make_celery 
from scripts import * 
import subprocess

#subprocess.call(["python", "/home/pi/Projects/Garbage_Detector/webapp/scripts/introScript.py"], shell=False)

app = Flask(__name__)
#This is used to set up the message broker
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
#This is to add the database for Celery to store its results into.
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = make_celery(app)


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

@app.route('/inputEmail')
def inputEmail():
    return render_template('inputEmail.html')

@app.route('/processInput')
def processInput():
    return render_template('processInput.html')

@app.route('/')
def frontPage():
    return render_template('parent.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
