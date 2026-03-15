from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm
from app.extensions import db
from app.models import Note
from app.services.security import save_pics_secure


def add_note(form: FlaskForm):
    user = current_user
    encrypted_content = g.encrypt.encrypt(form.content.data)
    note = Note(
        title = form.title.data, 
        user = user    
    )
    note.content = form.content.data
    note.cover_pic = save_pics_secure(form)
    try:
        db.session.add(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception
    
    
def delete_note(id : int):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception
    
    
def edit_note(form:FlaskForm, id: int):
    note = Note.query.get_or_404(id)
    note.title = form.title.data
    note.encrypted_content = g.encrypt.encrypt(form.content.data)
    pic_name = save_pics_secure(form)
    note.cover_pic = pic_name if pic_name is not None else note.cover_pic
    try:
        db.session.add(note)
        db.session.commit() 
    except Exception:
        db.session.rollback()
        raise Exception

def search_note(title):
    return Note.query.filter(Note.title.contains(title)).all()
