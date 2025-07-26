from flask_login import UserMixin
import logging
from app import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


logging.getLogger("pymongo").setLevel(logging.WARNING)

class User(UserMixin):
    collection = mongo.db.usuarios
    @staticmethod
    def create(nombre, email, password, role='user', profile_picture=None):
        user = {
            "nombre": nombre,
            "email": email,
            "password": generate_password_hash(password),
            "role": role,
            "profile_picture": profile_picture
        }
        User.collection.insert_one(user)

    def update(user_id, cambios):
        from bson.objectid import ObjectId
        User.collection.update_one({"_id": ObjectId(user_id)}, {"$set": cambios})    
        return User.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_by_email(email):
        return User.collection.find_one({"email": email})
    @staticmethod
    def find_by_id(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})
    @staticmethod
    def find_all():
        return User.collection.find()
    @staticmethod
    def find_by_role(role):
        return User.collection.find_one({"role": role})
    @staticmethod
    def find_one(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})
    
    def __init__(self, id, nombre, email, password, role='user', profile_picture=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.role = role
        self.profile_picture = profile_picture

    @staticmethod
    def from_dict(data):
        return User(
            id=str(data['_id']),
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            password=data.get('password', ''),
            role=data.get('role', 'user'),
            profile_picture=data.get('profile_picture', None)
        )