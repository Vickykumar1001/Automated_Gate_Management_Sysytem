from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key='your_secret_key'
    db.init_app(app)
    from .routes.index_routes import index as index_blueprint
    app.register_blueprint(index_blueprint)
    from .routes.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .routes.user_routes import user as user_blueprint
    app.register_blueprint(user_blueprint)
    with app.app_context():
        db.create_all()
        return app
