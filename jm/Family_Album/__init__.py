from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import main_views,face_registration_views,album_registration_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(face_registration_views.bp)
    app.register_blueprint(album_registration_views.bp)

    return app

# set FLASK_APP=Family_Album
# set FLASK_DEBUG=True
# set FLASK_RUN_PORT=5000