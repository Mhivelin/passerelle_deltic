"""
Script permettant d'ajouter manuellement un utilisateur à la base de données.
"""
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.extensions import db


if not User.query.filter_by(username="admin").first():
            new_user = User(username="admin", password=generate_password_hash("admin"))
            db.session.add(new_user)
            db.session.commit()