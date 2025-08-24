from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config
from .models import db
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals['os'] = os

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Force using the existing database, don't recreate it
    database_path = os.path.join(app.root_path, 'app.db')
    if not os.path.exists(database_path):
        raise FileNotFoundError(
            f"Database file not found at {database_path}. "
            "Please ensure app.db is pushed to the repository."
        )

    # Only create tables if they don't exist
    with app.app_context():
        from .models import User, Post
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import init_app_routes
    init_app_routes(app)

    return app
