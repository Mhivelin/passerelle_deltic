"""
Controlleur pour les routes des vue liées aux utilisateurs
"""

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, login_user, logout_user
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User



# Création d'un Blueprint pour le user controller
v_user_bp = Blueprint("user", __name__)


@v_user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Route pour afficher le formulaire de connexion"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('v_interface.home'))

        flash('Invalid username or password.')
        return redirect(url_for('user.login'))

    return render_template('login.html')


@v_user_bp.route("/app/login", methods=["POST"])
def app_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    return {'message': 'Invalid username or password'}, 401



@v_user_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Route pour afficher le formulaire d'inscription"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("user.login"))
    return render_template("register.html")


@v_user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))

