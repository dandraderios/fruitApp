from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app import mongo
from datetime import datetime, timedelta
import logging
from geopy.distance import geodesic

logging.basicConfig(
    format="%(asctime)s level=%(levelname)-7s "
    "threadName=%(threadName)s name=%(name)s %(message)s",
    level=logging.DEBUG,
)

ubicacion_bp = Blueprint('ubicacion', __name__)

@ubicacion_bp.route('/api/ubicacion', methods=['POST'])
@login_required
def guardar_ubicacion():
    mongo.db.ubicaciones_usuarios.create_index([("location", "2dsphere")])

    data = request.get_json()
    try:
        lat = float(data['lat'])
        lng = float(data['lng'])
    except (KeyError, ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Coordenadas inválidas'}), 400

    punto_actual = {
        "type": "Point",
        "coordinates": [lng, lat]
    }

    historial_doc = {
        "user_id": ObjectId(current_user.id),
        "location": punto_actual,
        "timestamp": datetime.utcnow()
    }

    mongo.db.ubicaciones_usuarios.insert_one(historial_doc)

    # Opcional: actualizar ubicación actual en usuarios
    mongo.db.usuarios.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": {"location": punto_actual}}
    )

    return jsonify({"status": "ok"})


@ubicacion_bp.route('/api/ubicacion/historico', methods=['GET'])
@login_required
def obtener_ubicaciones_historicas():
    # Parámetros opcionales: radio (en metros), centro (lat,lng), rango fecha
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radio_metros = request.args.get('radio', default=1000, type=float)  # 1 km
    dias = request.args.get('dias', default=30, type=int)  # últimos 30 días

    if lat is None or lng is None:
        return jsonify({'status': 'error', 'message': 'Faltan parámetros lat o lng'}), 400

    fecha_limite = datetime.utcnow() - timedelta(days=dias)

    query = {
        "user_id": ObjectId(current_user.id),
        "timestamp": {"$gte": fecha_limite},
        "location": {
            "$geoWithin": {
                "$centerSphere": [[lng, lat], radio_metros / 6378137]  # Radio en radianes (radio en metros / radio terrestre)
            }
        }
    }

    ubicaciones = list(mongo.db.ubicaciones_usuarios.find(query, {"_id": 0, "location": 1, "timestamp": 1}).sort("timestamp", -1))

    # Formatear resultado
    resultados = [
        {
            "lat": loc["location"]["coordinates"][1],
            "lng": loc["location"]["coordinates"][0],
            "timestamp": loc["timestamp"].isoformat()
        }
        for loc in ubicaciones
    ]

    return jsonify({"status": "ok", "ubicaciones": resultados})

@ubicacion_bp.route('/api/ubicacion/distancia-km0', methods=['POST'])
@login_required
def distancia_km0_api():
    data = request.get_json()
    lat_actual = data.get('lat')
    lng_actual = data.get('lng')
    if lat_actual is None or lng_actual is None:
        return jsonify({"error": "Faltan latitud o longitud"}), 400

    km0_santiago = (-33.442540, -70.653150)
    actual = (lat_actual, lng_actual)
    distancia_m = geodesic(actual, km0_santiago).meters

    return jsonify({
        "status": "ok",
        "distancia_metros": distancia_m,
        "distancia_km": round(distancia_m / 1000, 2)
    })