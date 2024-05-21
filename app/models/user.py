from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """
    Classe User qui permet de gérer les utilisateurs de l'application.


    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        """
        Méthode qui permet de hasher le mot de passe de l'utilisateur avant de le stocker en base de données.
        """
        self.password = generate_password_hash(password)


    def verify_password(self, password):
        """
        Méthode qui permet de vérifier si le mot de passe donné correspond au mot de passe stocké en base de données.
        si le mot de passe correspond, la méthode retourne True, sinon elle retourne False.
        """
        return check_password_hash(self.password, password)
