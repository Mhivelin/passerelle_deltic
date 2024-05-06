from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.

    Methods:
        set_password: Sets the password for the user.

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        """
        Sets the password for the user.

        Args:
            password (str): The password to set.

        Returns:
            None

        """
        self.password = generate_password_hash(password)
        
    
    def verify_password(self, password):
        """
        Verify the password of the user.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.

        """
        return check_password_hash(self.password, password)
