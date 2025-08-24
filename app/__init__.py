from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config, TestingConfig
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

    # Do NOT recreate an empty database file — use existing app.db
    # database_path = os.path.join(app.root_path, 'app.db')
    # if not os.path.exists(database_path):
    #     open(database_path, 'w').close()

    # Create database tables but DON'T override existing data
    with app.app_context():
        from .models import User, Post  # Import inside context to avoid circular import

        db.create_all()  # Create tables if they don't exist

        # Don't insert demo data if you already have your own
        # If you want demo data on a fresh db, uncomment below:
        # if not User.query.first():
        #     demo_user = User(username="DemoUser", email="demo@example.com", password="123456")
        #     db.session.add(demo_user)
        #     db.session.commit()
        #
        # if not Post.query.first():
        #     demo_post = Post(
        #         title="Welcome to Paw Forum!",
        #         content="This is your first demo post!",
        #         created_by=demo_user.id
        #     )
        #     db.session.add(demo_post)
        #     db.session.commit()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import inside function to avoid circular dependencies
        return User.query.get(int(user_id))

    from .routes import init_app_routes
    init_app_routes(app)

    return app
