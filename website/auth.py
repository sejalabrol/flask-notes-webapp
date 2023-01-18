from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        emailid = data["emailid"]
        password = data["pass"]

        user = User.query.filter_by(email=emailid).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect, try again", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        fname = data["fname"]
        pass1 = data["pass1"]
        pass2 = data["pass2"]

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")
        elif len(email) < 4:
            flash("email must be greater than 3 characters", category="error")
        elif len(fname) < 2:
            flash("first name must be greater than 1 character", category="error")
        elif pass1 != pass2:
            flash("passwords dont match", category="error")
        elif len(pass1) < 7:
            flash("password must be greater than 6 characters", category="error")
        else:
            # add user to database
            new_user = User(
                email=email,
                first_name=fname,
                password=generate_password_hash(pass1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("account created", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign-up.html", user=current_user)
