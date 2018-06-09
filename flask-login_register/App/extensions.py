from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
mail = Mail()


def config_extentions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = '请登录在访问'
    login_manager.session_protection = 'strong'

