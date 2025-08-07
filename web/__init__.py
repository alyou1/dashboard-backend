from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from src.models import db, User
from src import CONFIG
from web.api.connexion import auth

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG['SQLALCHEMY_TRACK_MODIFICATIONS']
    app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']

    # Init extensions
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Admin panel
    admin = Admin(app, name='Gestion des utilisateurs', template_mode='bootstrap3')
    with app.app_context():
        db.create_all()
        admin.add_view(ModelView(User, db.session))

    # Enregistrement du blueprint
    app.register_blueprint(auth)

    return app
