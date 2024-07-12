"""
Controlleur pour les routes des vues liées aux utilisateurs.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token
from flask_login import login_required, login_user, logout_user

from app.extensions import db  # pylint: disable=E0401
from app.models.user import User  # pylint: disable=E0401

# Création d'un Blueprint pour le user controller
v_user_bp = Blueprint("user", __name__)


@v_user_bp.route("/login", methods=["GET", "POST"])
def login():
    """Route pour afficher le formulaire de connexion et gérer la connexion"""
    # Si le formulaire est soumis
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for("v_interface.home"))

        # Afficher un message d'erreur si l'utilisateur
        # n'existe pas ou si le mot de passe est incorrect
        flash("Invalid username or password", "error")
        return redirect(url_for("user.login"))

    # Si la méthode est GET, afficher le formulaire de connexion
    return render_template("login.html")


@v_user_bp.route("/app/login", methods=["POST"])
def app_login():
    """Route pour la connexion d'un utilisateur via l'API"""
    # Récupérer les données du formulaire
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200
    return {"message": "Invalid username or password"}, 401


@v_user_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Route pour afficher le formulaire d'inscription et gérer l'inscription"""
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
    """Route pour déconnecter l'utilisateur"""
    logout_user()
    return redirect(url_for("user.login"))
