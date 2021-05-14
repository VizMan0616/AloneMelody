from datetime import date
from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    user_query = User.query.get(user_id)

    if not user_query:
        return Creator.query.get(user_id)

    return user_query


class User(db.Model, UserMixin):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.password}, {self.name})"
# Creator User


class Creator(db.Model, UserMixin):
    id = db.Column(db.String(15), primary_key=True)
    creator_name = db.Column(db.String(60), nullable=False)
    username_c = db.Column(db.String(20), unique=True, nullable=False)
    record_house = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False, default='null')
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    songs = db.relationship('Song', backref='uploader', lazy=True)

    def __repr__(self):
        return f"Creator('{self.username_c}', '{self.creator_name}', '{self.genre}', '{self.email}', '{self.password}')"

# Song


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(60), nullable=False)
    cover = db.Column(db.String(60), nullable=False)
    genre = db.Column(db.String(25), nullable=False)
    disco = db.Column(db.String(30), nullable=False)
    song_posted = db.Column(db.Date, nullable=False, default=date.today())
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)

    def __repr__(self):
        return f"Song('{self.song_title}', '{self.genre}', '{self.disco}')"

# Album


# class Album(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#  album_title = db.Column(db.String(60), nullable=False)
#    date_album = db.Column(db.Date, nullable=False)
#   discog = db.Column(db.String(60), nullable=False)
#    songs = db.relationship('Song', backref='album', lazy=True)
#    album_posted = db.Column(db.Date, nullable=False, default=date.today())
#    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)





