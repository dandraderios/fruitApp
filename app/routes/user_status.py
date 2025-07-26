from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app import mongo
import logging

logging.basicConfig(
    format="%(asctime)s level=%(levelname)-7s "
    "threadName=%(threadName)s name=%(name)s %(message)s",
    level=logging.DEBUG,
)

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/ping', methods=['POST'])
@login_required
def ping():
    logging.debug(f"Ping received from user: {current_user.id}")
    mongo.db.usuarios.update_one(
        {'_id': ObjectId(current_user.id)},
        {'$set': {'last_seen': datetime.utcnow()}}
    )
    return jsonify({'status': 'ok'})
