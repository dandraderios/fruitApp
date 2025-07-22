from flask_login import UserMixin
import logging

logging.getLogger("pymongo").setLevel(logging.WARNING)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        self.name = user_data.get("name", "")
