import logging
from logging.handlers import RotatingFileHandler
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from datetime import timedelta
from app.extensions import db
from app.models.user import User


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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config['SERVER_NAME'] = 'localhost:5000'

    app.config["SECRET_KEY"] = "deltictmp"
    db.init_app(app)

    # Configurer les logs
    configure_logs(app)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    app.logger.setLevel(logging.DEBUG)


    # initialisation du JWT
    app.config["JWT_SECRET_KEY"] = "deltictmp"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)




    with app.app_context():
        db.create_all()


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
        if not User.query.filter_by(username="admin").first():
            new_user = User(username="admin")
            new_user.set_password("admin")
            db.session.add(new_user)
            db.session.commit()






    return app
