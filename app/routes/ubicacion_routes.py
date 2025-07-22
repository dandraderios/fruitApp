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

ubicacion_bp = Blueprint('ubicacion', __name__)

@ubicacion_bp.route('/api/ubicacion', methods=['POST'])
@login_required
def guardar_ubicacion():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    logging.debug(f"Current user: {current_user.id}")
    mongo.db.usuarios.update_one(
        {'_id': ObjectId(current_user.id)},
        {'$set': {'coordenadas': {'lat': data['lat'], 'lon': data['lng']}}}
    )
    return jsonify({'status': 'ok'})
