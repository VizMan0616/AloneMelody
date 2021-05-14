from flask import (Blueprint, render_template, url_for, redirect, request, abort)
from .forms import LoginForm
from ..models import *
from .. import db, bcrypt, utils
from flask_login import (login_user, current_user, logout_user, login_required)
from ..models import *

home = Blueprint("home", __name__)


@home.route('/')
@home.route("/home")
def homepage():
    songs = db.session.query(Song).all()
    songs_len = len(songs)
    if current_user.is_authenticated:
        return render_template("homepage.html", songs=songs, songs_len=songs_len)
    else:
        return render_template("home.html")


@home.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home.homepage"))

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = Creator.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home.homepage"))

    return render_template("login.html", form=form, title="Iniciar Sesion")


@home.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.homepage"))


@home.route("/song/<id>/delete")
def delete_song(id):
    song = Song.query.get_or_404(id)

    if song.uploader != current_user:
        abort(403)
    db.session.delete(song)
    db.session.commit()
    db.session.flush()
    return redirect(url_for('home.homepage')) if request.url_rule.endpoint == 'home.homepage' else redirect(url_for('c_creator.musician_profile'))

