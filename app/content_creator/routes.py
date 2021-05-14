import os
from flask import (Blueprint, render_template, redirect, url_for, request)
from .forms import RegisterForm, UpdateForm, SongForm
from ..models import Creator, Song
from flask_login import current_user, login_required
from ..import db, bcrypt, utils

c_creator = Blueprint("c_creator", __name__)


@c_creator.route("/register/content_creator", methods=["GET", "POST"])
def register_creator():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.cfrm_password.data).decode('utf-8')
        creator = Creator(id=utils.generate_id("CU"),
                          creator_name=form.full_name.data,
                          username_c=form.username.data,
                          record_house=form.disco.data,
                          email=form.email.data,
                          creation_date=form.creation_date.data,
                          password=hashed_password)

        os.mkdir(f'D:\\Python_Projects\\AloneMelody\\app\\static\\music\\{creator.id}')
        db.session.add(creator)
        db.session.commit()
        db.session.flush()
        return redirect(url_for('home.login'))

    return render_template("register_creator.html", form=form, title="Para Creadores de Contenido")


@c_creator.route("/profile_musician", methods=["GET", "POST"])
@login_required
def musician_profile():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username_c = form.username.data
        current_user.record_house = form.disco.data
        current_user.email = form.email.data
        current_user.description = form.description.data

        if form.pfp.data:
            pfp = utils.save_picture(form.pfp.data)
            current_user.profile_pic = pfp

        db.session.commit()
        db.session.flush()
        return redirect(url_for("c_creator.musician_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username_c
        form.disco.data = current_user.record_house
        form.email.data = current_user.email

    pfp = f'img/pfp/{current_user.profile_pic}'
    return render_template("profile_creator.html", form=form, pfp=pfp, title=current_user.username_c)


@c_creator.route("/profile_musician/add_song", methods=["GET", "POST"])
def add_song():
    form = SongForm()

    if form.validate_on_submit():
        cover_file = utils.save_cover(form.song_cover.data)
        song = Song(song_title=form.song_title.data,
                    cover=cover_file,
                    genre=form.song_genre.data,
                    disco=form.disco.data,
                    creator_id=current_user.id)

        utils.save_song(form.save_song.data, current_user.id, form.song_title.data.replace(" ", ""))
        db.session.add(song)
        db.session.commit()
        db.session.flush()
        return redirect(url_for("c_creator.musician_profile"))

    return render_template("add_song.html", form=form, title="Agregar Cancion")


@c_creator.route("/song")
def song_view():
    songs = db.session.query(Song)
    songz = [i for i in songs if current_user.id == i.uploader.id]
    songz_len = len(songz)
    return render_template("creator_songs.html", songs=songz, songs_len=songz_len)
