from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import logging
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta

logging.basicConfig(
    format="%(asctime)s level=%(levelname)-7s "
    "threadName=%(threadName)s name=%(name)s %(message)s",
    level=logging.DEBUG,
)

oauth = OAuth()

def configure_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://openidconnect.googleapis.com/v1/',  # URL base para API Google OpenID
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # URL completa
        client_kwargs={'scope': 'openid email profile'}
    )

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = mongo.db.usuarios.find_one({'email': request.form['email']})
        if user_data and check_password_hash(user_data['password'], request.form['password']):
            user = User(str(user_data.get("_id")), user_data.get('nombre'), user_data.get('email'), user_data.get('password'))
            login_user(user, remember=True, duration=timedelta(days=30))
            return redirect(url_for('main.index'))
        flash('Credenciales inválidas', 'warning')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hash_pass = generate_password_hash(request.form['password'])
        mongo.db.usuarios.insert_one({
            'email': request.form['email'],
            'password': hash_pass,
            'name': request.form.get('name', '')
        })
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
        userinfo = oauth.google.get('userinfo').json()

        email = userinfo['email']
        name = userinfo.get('name', '')
        profile_picture = userinfo.get('picture', '')
        logging.info(f"Google user info: {userinfo}")
        logging.info(f"User email: {email}, Name: {name}, Profile Picture: {profile_picture}")

        # Buscar o crear usuario
        user_data = User.find_by_email(email)
        logging.info(f"User data found: {user_data}")
        if not user_data:
            User.create(email=email, password='', nombre=name, role='user', profile_picture=profile_picture)
            user_data = User.find_by_email(email)
            logging.info(f"New user created: {user_data['email']}")
        else:
            # Actualizar nombre y foto si cambiaron
            logging.info(f"User found: {user_data['email']}")
            cambios = {}
            if user_data.get('nombre') != name:
                cambios['nombre'] = name
            if user_data.get('profile_picture') != profile_picture:
                cambios['profile_picture'] = profile_picture
            if cambios:
                User.update(user_data['_id'], cambios)

        user = User(
            id=str(user_data['_id']),
            nombre=user_data.get('nombre', name),
            email=email,
            password=user_data.get('password', ''),
            role=user_data.get('role', 'user'),
            profile_picture=profile_picture
        )
        logging.info(f"Logging in user: {user.email}")
        login_user(user, remember=True, duration=timedelta(days=30))
        return redirect(url_for('main.index'))  # o 'dashboard'

    except Exception as e:
        flash(f'Error en login con Google: {str(e)}', 'danger')
        logging.error(f"Error during Google login: {str(e)}")
        return redirect(url_for('auth.login'))