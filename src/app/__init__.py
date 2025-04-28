#Archived script
from flask import Flask
from app.routes import main_blueprint
from app.models import load_models

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    #load ml and add to app 
    app.rf_model, app.vectorizer = load_models()

    #reg blueprints
    app.register_blueprint(main_blueprint)
    return app