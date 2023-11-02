from flask import Flask
from .views import face_registration_views_integ, main_views_integ
from config import Config

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    from .views import main_views_integ,face_registration_views_integ,album_registration_views_integ,album_inquiry_views_integ
    app.register_blueprint(main_views_integ.bp)
    app.register_blueprint(face_registration_views_integ.bp)
    app.register_blueprint(album_registration_views_integ.bp)
    app.register_blueprint(album_inquiry_views_integ.bp)

    app.config.from_object('config.DevConfig')

    return app

# set FLASK_APP=Family_Album
# set FLASK_DEBUG=True
# set FLASK_RUN_PORT=5000