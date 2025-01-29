"""Module with login templates."""
from flask import render_template, redirect, url_for, session, request, flash, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from .classes import User, Library
from .file_manager import get_name_pass, save_user

bp = Blueprint('auth', __name__)

users : dict[str, str] = get_name_pass()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username is in use!', 'danger')
        else:
            users[username] = generate_password_hash(password)
            save_user(User({
                'username' : username,
                'password' : generate_password_hash(password),
                'library' : Library([]).to_dict()
            }))
            flash('Signup successful!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html')
