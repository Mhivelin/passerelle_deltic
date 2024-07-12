"""
Ce fichier contient la configuration de l'application Flask.
"""

import logging
import os
import socket
import sys
from datetime import timedelta
from logging.handlers import RotatingFileHandler

import dotenv
from flask import Flask, render_template, request
# from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from prometheus_client import Counter, make_wsgi_app
# from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app.extensions import db
from app.models.database import create_database
from app.models.user import User

dotenv.load_dotenv(dotenv.find_dotenv())

# Define Prometheus counters for logs
INFO_LOG_COUNT = Counter("info_log_count", "Number of info log entries")
WARNING_LOG_COUNT = Counter("warning_log_count", "Number of warning log entries")
ERROR_LOG_COUNT = Counter("error_log_count", "Number of error log entries")


class PrometheusLoggingHandler(logging.Handler):
    """
    Création d'un handler pour les logs qui incrémente les compteurs Prometheus.
    """

    def emit(self, record):
        if record.levelno == logging.INFO:
            INFO_LOG_COUNT.inc()
        elif record.levelno == logging.WARNING:
            WARNING_LOG_COUNT.inc()
        elif record.levelno == logging.ERROR:
            ERROR_LOG_COUNT.inc()


def configure_logs(app):
    """
    Configure the logging for the Flask application.
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # StreamHandler for sending logs to stdout (useful for Docker)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

    # Optional: FileHandler for writing logs to a file
    file_handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Add Prometheus logging handler
    prometheus_handler = PrometheusLoggingHandler()
    prometheus_handler.setFormatter(formatter)
    app.logger.addHandler(prometheus_handler)

    app.logger.info("Configuration des logs terminée.")


def get_ip_address():
    """
    Get the IP address of the current machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except socket.error as e:
        print(f"Erreur de socket: {e}")
        ip_address = "N/A"
    finally:
        s.close()
    return ip_address


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    db.init_app(app)

    # Configure Prometheus metrics exporter
    # metrics = PrometheusMetrics(app)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    # Configure logs
    configure_logs(app)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    app.logger.setLevel(logging.DEBUG)

    @app.before_request
    def override_method():
        if "_method" in request.form:
            method = request.form["_method"].upper()
            if method in ["PUT", "DELETE"]:
                request.environ["REQUEST_METHOD"] = method

    # JWT initialization
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    # jwt = JWTManager(app)

    ip = os.getenv("IP") if os.getenv("IP") else get_ip_address()

    app.config["SERVER_NAME"] = f"{ip}:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"

    # Create the database
    with app.app_context():
        db.create_all()
        create_database()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_error_handler(
        404, lambda error: (render_template("error/404.html"), 404)
    )
    app.register_error_handler(
        500, lambda error: (render_template("error/500.html"), 500)
    )

    register_blueprints(app)

    with app.app_context():
        create_admin_user(app)

    return app


def register_blueprints(app):
    """
    Register all blueprints for the application.
    """
    from app.controllers.client_controller import \
        client_bp  # pylint: disable=C0415
    from app.controllers.database_controller import \
        database_bp  # pylint: disable=C0415
    from app.controllers.ebp_controller import ebp_bp  # pylint: disable=C0415
    from app.controllers.main_controller import \
        main_bp  # pylint: disable=C0415
    from app.controllers.passerelle_controller import \
        passerelle_bp  # pylint: disable=C0415
    from app.controllers.sellsy_controller import \
        sellsy_bp  # pylint: disable=C0415
    from app.controllers.vues_controller.v_client_controller import \
        v_client_bp  # pylint: disable=C0415
    from app.controllers.vues_controller.v_interface_controller import \
        v_interface_bp  # pylint: disable=C0415
    from app.controllers.vues_controller.v_logiciel_controller import \
        v_logiciel_bp  # pylint: disable=C0415
    from app.controllers.vues_controller.v_passerelle_controller import \
        v_passerelle_bp  # pylint: disable=C0415
    from app.controllers.vues_controller.v_user_controller import \
        v_user_bp  # pylint: disable=C0415
    from app.controllers.zeendoc_controller import \
        zeendoc_bp  # pylint: disable=C0415

    app.register_blueprint(main_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(ebp_bp)
    app.register_blueprint(zeendoc_bp)
    app.register_blueprint(database_bp)
    app.register_blueprint(passerelle_bp)
    app.register_blueprint(sellsy_bp)

    app.register_blueprint(v_interface_bp)
    app.register_blueprint(v_client_bp)
    app.register_blueprint(v_logiciel_bp)
    app.register_blueprint(v_passerelle_bp)
    app.register_blueprint(v_user_bp)


def create_admin_user(app):
    """
    Create the admin user if it does not exist.
    """
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if username is None or password is None:
        app.logger.error("ADMIN_USERNAME ou ADMIN_PASSWORD non définis dans .env")
        raise ValueError(
            "ADMIN_USERNAME ou ADMIN_PASSWORD doivent être définis dans le fichier .env"
        )

    if not User.query.filter_by(username=username).first():
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info("Nouvel utilisateur admin ajouté avec succès.")
