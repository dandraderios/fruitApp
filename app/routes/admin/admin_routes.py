from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import mongo
from datetime import datetime
from bson.objectid import ObjectId
import config

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/')
@login_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/exportadoras/register', methods=['GET', 'POST'])
@login_required
def register_exportadora():
    if request.method == 'POST':
        data = request.form

        # Extraer comisión por tramos
        desde_list = data.getlist('desde[]')
        hasta_list = data.getlist('hasta[]')
        porcentaje_list = data.getlist('porcentaje[]')
        comision = {}

        for desde, hasta, porcentaje in zip(desde_list, hasta_list, porcentaje_list):
            tramo = f"{desde.strip()}-{hasta.strip()}"
            comision[tramo] = float(porcentaje)

        exportadora = {
            "razon_social": data.get('razon_social'),
            "rut": data.get('rut'),
            "direccion": data.get('direccion'),
            'detalle_direccion': data.get('detalle_direccion'),
            "comuna": data.get('comuna'),
            "region": data.get('region'),
            "coordenadas": {
                "lat": float(data.get('lat')) if data.get('lat') else None,
                "lng": float(data.get('lng')) if data.get('lng') else None
            },
            "tipo": data.get('tipo'),
            "status": data.get('status'),
            "comisiones": comision,
            "contacto": data.get('contacto'),
            "email_notificaciones": data.get('email_notificaciones'),
            "api_config": {
                "url": data.get('url_api'),
                "user": data.get('user_api'),
                "clave": data.get('clave_api')
            },
            "fecha_creacion": datetime.utcnow()
        }

        # Validación mínima
        if not exportadora["razon_social"] or not exportadora["rut"]:
            flash("Razon social y RUT son obligatorios", "danger")
            return render_template('admin/register_exportadora.html')

        # Insertar en Mongo
        mongo.db.exportadoras.insert_one(exportadora)

        flash("Exportadora registrada correctamente", "success")
        return redirect(url_for('admin.register_exportadora'))

    return render_template('admin/register_exportadora.html', GOOGLE_MAPS_API_KEY=config.GOOGLE_MAPS_API_KEY)


@admin_bp.route('/admin/exportadoras/<exportadora_id>/edit', methods=['GET', 'POST'])
def editar_exportadora(exportadora_id):
    exportadora = mongo.db.exportadoras.find_one({'_id': ObjectId(exportadora_id)})
    if not exportadora:
        flash('Exportadora no encontrada.', 'danger')
        return redirect(url_for('admin.editar_exportadora', exportadora_id=exportadora_id))

    if request.method == 'POST':
        data = request.form.to_dict(flat=False)

        exportadora['razon_social'] = request.form.get('razon_social')
        exportadora['rut'] = request.form.get('rut')
        exportadora['direccion'] = request.form.get('direccion')
        exportadora['detalle_direccion'] = request.form.get('detalle_direccion')
        exportadora['region'] = request.form.get('region')
        exportadora['comuna'] = request.form.get('comuna')
        exportadora['lat'] = float(request.form.get('lat'))
        exportadora['lng'] = float(request.form.get('lng'))
        exportadora['tipo'] = request.form.get('tipo')
        exportadora['status'] = request.form.get('status')
        exportadora['contacto'] = request.form.get('contacto')
        exportadora['email_notificaciones'] = request.form.get('email_notificaciones')
        exportadora['url_api'] = request.form.get('url_api')
        exportadora['user_api'] = request.form.get('user_api')
        exportadora['clave_api'] = request.form.get('clave_api')

        # Manejo de comisiones
        desde = request.form.getlist('desde[]')
        hasta = request.form.getlist('hasta[]')
        porcentaje = request.form.getlist('porcentaje[]')
        comisiones = []
        for d, h, p in zip(desde, hasta, porcentaje):
            try:
                comisiones.append({
                    'desde': int(d),
                    'hasta': int(h),
                    'porcentaje': float(p)
                })
            except ValueError:
                continue
        exportadora['comisiones'] = comisiones

        mongo.db.exportadoras.update_one({'_id': ObjectId(exportadora_id)}, {'$set': exportadora})
        flash('Exportadora actualizada correctamente.', 'success')
        return redirect(url_for('admin.index'))

    return render_template('admin/edit_exportadora.html', exportadora=exportadora, GOOGLE_MAPS_API_KEY=config.GOOGLE_MAPS_API_KEY)