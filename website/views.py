from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        data = request.form
        note = data["note"]
        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully", category="success")

    return render_template("home.html", user=current_user)


@views.route("/delete_note")
@login_required
def delete_note():
    note_id = request.args.get("note_id")
    note_to_delete = Note.query.get(note_id)
    if note_to_delete:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()
    return redirect(url_for("views.home"))
