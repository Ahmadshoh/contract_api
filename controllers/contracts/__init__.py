from flask import Blueprint

bp = Blueprint('contracts', __name__)

from controllers.contracts import routes
