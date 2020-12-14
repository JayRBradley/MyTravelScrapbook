from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countryID = db.Column(db.Integer, db.ForeignKey("country.id"))
    name = db.Column(db.String(64), index=True)
    post = db.relationship("Post", backref="City", lazy="dynamic")


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    city = db.relationship("City", backref="Country", lazy="dynamic")
    user = db.relationship("User", backref="Country", lazy="dynamic")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    blog = db.Column(db.String(64), index=True)
    StartDate = db.Column(db.DateTime())
    EndDate = db.Column(db.DateTime())
    cityID = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    countryID = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    post = db.relationship('Post', backref='User', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


