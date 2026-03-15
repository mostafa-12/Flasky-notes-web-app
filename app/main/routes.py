from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.main.forms import UpdateProfileForm, NoteForm
from app.models import Note
from app.services.user import update_user
from app.services import note
from app.main import main


@main.route("/")
def home():
    return render_template("main/home.html", title="Home")

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        # Handle profile update logic here (e.g., save changes to the database)
        if update_user(form):
            flash("Profile updated successfully!", "success")
        else:
            flash("Failed to update profile. Please try again.", "danger")
        return redirect(url_for("main.profile"))
    return render_template("main/profile.html", title="Profile", form=form)


@main.route("/notes")
@login_required
def notes():
    notes = current_user.notes.all()
    return render_template("main/notes.html", title = "Notes page", notes=notes)

@main.route("/add_note", methods=["GET", "POST"])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note.add_note(form)
        flash("Note added successfully!", "success")
        return redirect(url_for("main.notes"))
    return render_template("main/add_note.html", title = "Add Note", form=form)


@main.route("/notes/show/<int:note_id>")
@login_required
def show_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template("main/note.html", title=note.title, note=note)

@main.route("/notes/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    note.delete_note(note_id)
    flash("Note deleted successfully!", "success")
    return redirect(url_for("main.notes"))

@main.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    _note = Note.query.get_or_404(note_id)
    form = NoteForm()
    if form.validate_on_submit():
        note.edit_note(form, note_id)
        flash("Note updated successfully!", "success")
        return redirect(url_for("main.notes"))
    form.title.data = _note.title
    form.content.data = _note.content
    return render_template("main/edit_note.html", title="Edit Note", form=form)