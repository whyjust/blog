from flask import Flask,render_template
from App.settings import config
from App.extensions import config_extentions
from App.views import config_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config_extentions(app)
    config_blueprint(app)
    errors(app)
    return app

def errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/error.html',error=e)
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/error.html', error=e)