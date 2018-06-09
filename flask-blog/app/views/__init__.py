from .main import main
from .user import user
from .posts import posts

BluePrint = [
    (main,''),
    (user,''),
    (posts,'')
]

#封装注册蓝本的函数
def config_blueprint(app):
    #循环注册蓝本
    for blueprint,prefix in BluePrint:
        app.register_blueprint(blueprint,url_prefix=prefix)