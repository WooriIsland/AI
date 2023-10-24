from flask import Flask
from .views import main_views_pc1

def create_app():
    app = Flask(__name__)

    from .views import album_registration_views_pc1
    app.register_blueprint(main_views_pc1.bp)
    app.register_blueprint(album_registration_views_pc1.bp)

    return app