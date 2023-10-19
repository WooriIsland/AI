from flask import Flask
from .views import face_registration_views_integ, main_views_integ

def create_app():
    app = Flask(__name__)

    from .views import main_views_integ,face_registration_views_integ,album_registration_views_integ
    app.register_blueprint(main_views_integ.bp)
    app.register_blueprint(face_registration_views_integ.bp)
    app.register_blueprint(album_registration_views_integ.bp)

    return app

# set FLASK_APP=Family_Album
# set FLASK_DEBUG=True
# set FLASK_RUN_PORT=5000