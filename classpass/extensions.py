from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "common.login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
sess = Session()
cors = CORS()
