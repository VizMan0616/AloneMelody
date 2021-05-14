from flask import Flask
from .Config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "home.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .home.routes import home
    from .users.routes import users
    from .content_creator.routes import c_creator

    app.register_blueprint(home)
    app.register_blueprint(users)
    app.register_blueprint(c_creator)

    return app

