from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import mongo

ubicacion_bp = Blueprint('ubicacion', __name__)

@ubicacion_bp.route('/ubicacion', methods=['POST'])
@login_required
def guardar_ubicacion():
    data = request.get_json()
    mongo.db.usuarios.update_one(
        {'_id': current_user.id},
        {'$set': {'coordenadas': {'lat': data['lat'], 'lon': data['lon']}}}
    )
    return jsonify({'status': 'ok'})
