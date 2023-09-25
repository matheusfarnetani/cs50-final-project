import os

from flask import Flask
from .extensions import db, migrate, bcrypt, sess, cors, login_manager

# Blueprints
from .blueprints.api.routes import api_bp
from .blueprints.auth.routes import auth_bp
from .blueprints.common.routes import common_bp
from .blueprints.graphs.routes import graphs_bp
from .blueprints.tables.routes import tables_bp

# File path to databases
file_path = os.path.abspath(os.path.join(os.getcwd(), "classpass/database/classpass.db"))

def create_app():

    # Create App
    app = Flask(__name__)

    # Configure
    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Init extensions
    sess.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)

    # Add Blueprint
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(graphs_bp)
    app.register_blueprint(tables_bp)

    # Return app
    return app
