import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AVATAR_FOLDER = os.path.join(BASE_DIR, 'static', 'image', 'avatars')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'image', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'tests')
