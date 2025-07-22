from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = mongo.db.usuarios.find_one({'email': request.form['email']})
        if user_data and check_password_hash(user_data['password'], request.form['password']):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Credenciales inválidas')
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
