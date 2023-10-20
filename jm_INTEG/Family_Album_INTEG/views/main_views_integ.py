from flask import Flask
from flask import Blueprint

bp = Blueprint('main_integ',__name__,url_prefix='/')

@bp.route('/home')
def hello_woori():
    return 'Welcome to Woori-Family-Island'
