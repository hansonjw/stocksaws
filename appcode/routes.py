import functools
from flask import render_template, Blueprint, redirect

bp = Blueprint('routes', __name__, url_prefix='')

@bp.route('/base', methods=(['GET']))
def home():
    return render_template('base.html')