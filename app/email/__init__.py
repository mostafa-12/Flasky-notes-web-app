from flask import Blueprint

Email = Blueprint("email", __name__)

from . import routes