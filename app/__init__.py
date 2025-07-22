from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_cors import CORS

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    from .routes.auth_routes import auth_bp
    from .routes.oferta_routes import oferta_bp
    from .routes.ubicacion_routes import ubicacion_bp
    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(oferta_bp)
    app.register_blueprint(ubicacion_bp)

    return app
