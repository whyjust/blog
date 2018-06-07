from .user import user
from .main import main

BluePrint = [
    (user,''),
    (main,'')
]

def config_blueprint(app):
    for blueprint,prefix in BluePrint:
        app.register_blueprint(blueprint,url_prefix=prefix)