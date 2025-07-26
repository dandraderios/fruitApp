from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config
from bson.objectid import ObjectId

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirige si no está logueado
login_manager.login_message_category = 'warning'
login_manager.session_protection = 'strong'  # protección de sesión fuerte
login_manager.refresh_view = 'auth.login'  # refresca la sesión si está inactiva
login_manager.needs_refresh_message = "Por favor, vuelve a iniciar sesión para continuar."
login_manager.needs_refresh_message_category = 'warning'  # categoría del mensaje de refresco
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = 'warning'  # categoría del mensaje de login
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp, configure_oauth
    from app.routes.ubicacion_routes import ubicacion_bp
    from app.routes.user_status import status_bp
    from app.routes.admin.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    configure_oauth(app)
    app.register_blueprint(ubicacion_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(admin_bp)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.usuarios.find_one({"_id": ObjectId(user_id)})
        return User.from_dict(user_data) if user_data else None

    return app

from bson.objectid import ObjectId
