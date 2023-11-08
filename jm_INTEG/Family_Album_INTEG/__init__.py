from flask import Flask
from config import Config
# import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    from .views import main_views_integ,face_registration_views_integ,album_registration_views_integ,album_inquiry_views_integ,album_update_views_integ,album_delete_views_integ,album_search_views_integ
    app.register_blueprint(main_views_integ.bp)
    app.register_blueprint(face_registration_views_integ.bp)
    app.register_blueprint(album_registration_views_integ.bp)
    app.register_blueprint(album_inquiry_views_integ.bp)
    app.register_blueprint(album_update_views_integ.bp)
    app.register_blueprint(album_delete_views_integ.bp)
    app.register_blueprint(album_search_views_integ.bp)

    app.config.from_object('config.DevConfig')

    return app

# set FLASK_APP=Family_Album
# set FLASK_DEBUG=True
# set FLASK_RUN_PORT=5000