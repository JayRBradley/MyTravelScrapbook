
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    artists = db.relationship('Artist', backref='city', lazy='dynamic')
    venues = db.relationship('Venue', backref='city', lazy='dynamic')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(64), index=True)
    cityID = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    artistToEvent = db.relationship('ArtistToEvent', backref='artist', lazy='dynamic')


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    cityID = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    events = db.relationship('Event', backref='venue', lazy='dynamic')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    time = db.Column(db.DateTime())
    venueID = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artistsToEvent = db.relationship('ArtistToEvent', backref='event', lazy='dynamic')

class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    eventID = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))