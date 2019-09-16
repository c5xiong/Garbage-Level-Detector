import os
basedir = os.path.abspath(os.path.dirname(__file__))

#This is to be able to access the database itself
class Config(object):

    #This database is designed to get the URL of the database or
    #establish a new instance of the database. 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'dataBase.db')
    #This variable is designed to indicate that a change is about to be made
    #to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

