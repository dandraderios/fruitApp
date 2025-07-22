from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.ubicacion_routes import ubicacion_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ubicacion_bp)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.usuarios.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None

    return app

from bson.objectid import ObjectId
