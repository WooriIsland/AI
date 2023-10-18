from flask import Blueprint

bp = Blueprint('main_pc1',__name__,url_prefix='/')

@bp.route('/')
def hello_woori_pc1():
    return 'Welcome to Woori-Family-Island-PC1'