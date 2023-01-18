from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        emailid = data["emailid"]
        password = data["pass"]
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "logout page"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        fname = data["fname"]
        pass1 = data["pass1"]
        pass2 = data["pass2"]
        if len(email) < 4:
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
            flash("account created", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign-up.html")
