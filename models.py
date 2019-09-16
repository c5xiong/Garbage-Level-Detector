from app import db


class User(db.Model):
    #the variable name is a field while db.Integer/String/... is the field type
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    listOfEmails = db.relationship('Post', backref='authpr', lazy='dynamic')

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
