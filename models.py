from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#Flask-Login always keeps track of the logged in user by storing the login's unique
#identifier in Flask's user session which is a storage space that is assigned 
#to each connected user. In short, whenever a user logs into the application, Flask
#will retrive its id from this storage and load into memory. The loader is register
# with @login.user_loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    #the variable name is a field while db.Integer/String/... is the field type
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    listOfEmails = db.relationship('Post', backref='author', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #body = db.Column(db.String(140))
    email = db.Column(db.String, primary_key=True)
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
