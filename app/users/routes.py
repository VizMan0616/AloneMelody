from flask import (Blueprint, render_template, url_for, request, redirect, flash)
from .forms import (RegistrationForm, UpdateForm)
from ..models import *
from datetime import date
from .. import db, bcrypt, utils
from flask_login import current_user, login_required


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.cfrm_password.data).decode('utf-8')

        user = User(id=utils.generate_id("RU"),
                    name=form.full_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    sex=form.sex.data,
                    date=form.birth_date.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.login'))
    return render_template("register.html", form=form, title="Registrarse")

# @users.route("/profile")
# def user_profile():
#    form = UpdateForm()
#    pfp = f'img/pfp/{current_user.profile_pic}'
#    return render_template("profile.html", pfp=pfp, form=form)


@users.route("/profile", methods=["GET", "POST"])
def user_profile():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.name = form.full_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.pfp.data:
            pfp = utils.save_picture(form.pfp.data)
            current_user.profile_pic = pfp

        db.session.commit()
        db.session.flush()
        return redirect(url_for("users.user_profile"))
    elif request.method == 'GET':
        form.full_name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    pfp = f'img/pfp/{current_user.profile_pic}'
    return render_template("profile.html", form=form, pfp=pfp)


@users.route("/search")
def search_results():
    query = request.args.get("search_bar")
    return render_template("search_results.html", query_result=query, title=f"Find {query}")
