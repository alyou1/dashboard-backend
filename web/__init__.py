from flask import Flask
from flask_migrate import Migrate
from src.models import db
from src import CONFIG

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['SQLALCHEMY_DATABASE_URI']
    # set optional bootswatch theme
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG['SQLALCHEMY_TRACK_MODIFICATIONS']
    app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']
    db.init_app(app)
    Migrate(app,db)
    with app.app_context():
        db.create_all()

    return app
