from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from recipeezy.db import get_db

bp = Blueprint('main_router', __name__)

@bp.route('/')
def index():
    db = get_db()
    return render_template('templates/home.html')