from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import requests
import logging
from datetime import timedelta

logging.basicConfig(
    format="%(asctime)s level=%(levelname)-7s "
    "threadName=%(threadName)s name=%(name)s %(message)s",
    level=logging.DEBUG,
)

main_bp = Blueprint('main', __name__)
API_BASE = "https://apis.digital.gob.cl/dpa"

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@main_bp.route('/get_iframe_attributes', methods=['OPTIONS', 'GET'])
@login_required
def dummy_iframe():
    return '', 204

@main_bp.route('/regiones')
def obtener_regiones():
    url = f"{API_BASE}/regiones"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MiApp/1.0)'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/comunas/<region_codigo>')
def obtener_comunas_por_region(region_codigo):
    region_codigo = region_codigo.strip().upper()
    logging.info("Region code: " + region_codigo)
    if not region_codigo:
        return jsonify({"error": "Falta parámetro region"}), 400

    url = f"{API_BASE}/regiones/{region_codigo}/comunas"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MiApp/1.0)'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        comunas = resp.json()
        return jsonify(comunas)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500