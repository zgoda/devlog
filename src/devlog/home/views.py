from flask import render_template

from . import home_bp


@home_bp.route('/')
def index():
    context = {}
    return render_template('index.html', **context)
