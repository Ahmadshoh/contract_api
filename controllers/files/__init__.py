from flask import Blueprint

bp = Blueprint('files', __name__)

from controllers.files import routes
