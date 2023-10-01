import os
import config

from flask import Flask

from .api.routes import api
from .api.models import setup_db

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or config.SECRET_KEY
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') or config.DATABASE_URI
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.register_blueprint(api)
	setup_db(app)
	return app
