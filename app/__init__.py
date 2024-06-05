import logging
from logging.handlers import RotatingFileHandler
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
import os
import dotenv
from datetime import timedelta
from app.extensions import db
from app.models.user import User
from app.models.database import create_database

dotenv.load_dotenv(dotenv.find_dotenv())

def configure_logs(app):
    # Formatter pour les logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # StreamHandler pour envoyer les logs à stdout (utile pour Docker)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)  # Modifier si nécessaire
    app.logger.addHandler(stream_handler)

    # Facultatif: FileHandler pour écrire les logs dans un fichier
    file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.info("Configuration des logs terminée.")






def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    # app.config['SERVER_NAME'] = 'localhost:5000'

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    db.init_app(app)

    # Configurer les logs
    configure_logs(app)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    app.logger.setLevel(logging.DEBUG)


    # initialisation du JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'https'



    # création de la base de données

    with app.app_context():
        db.create_all()
        create_database()


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_error_handler(404, lambda error: (render_template("error/404.html"), 404))
    app.register_error_handler(500, lambda error: (render_template("error/500.html"), 500))

    from app.controllers.client_controller import client_bp
    from app.controllers.ebp_controller import ebp_bp
    from app.controllers.zeendoc_controller import zeendoc_bp
    from app.controllers.database_controller import database_bp

    # vues
    from app.controllers.vues_controller.v_interface_controller import v_interface_bp
    from app.controllers.vues_controller.v_client_controller import v_client_bp
    from app.controllers.vues_controller.v_logiciel_controller import v_logiciel_bp
    from app.controllers.vues_controller.v_passerelle_controller import v_passerelle_bp
    from app.controllers.vues_controller.v_user_controller import v_user_bp

    app.register_blueprint(client_bp)
    app.register_blueprint(ebp_bp)
    app.register_blueprint(zeendoc_bp)
    app.register_blueprint(database_bp)

    app.register_blueprint(v_interface_bp)
    app.register_blueprint(v_client_bp)
    app.register_blueprint(v_logiciel_bp)
    app.register_blueprint(v_passerelle_bp)
    app.register_blueprint(v_user_bp)



    # ajout d'un utilisateur
    with app.app_context():
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        if username is None or password is None:
            app.logger.error("ADMIN_USERNAME ou ADMIN_PASSWORD non définis dans .env")
            raise ValueError("ADMIN_USERNAME ou ADMIN_PASSWORD doivent être définis dans le fichier .env")

        if not User.query.filter_by(username=username).first():
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            app.logger.info("Nouvel utilisateur admin ajouté avec succès.")






    return app
