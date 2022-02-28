from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from recipeezy.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/home', methods=('GET', 'POST'))
def index():
    return render_template('/home.html')