from flask import Flask,render_template
from app.settings import config
from app.extensions import config_extensions
from app.views import config_blueprint


#初始化当前整个应用的函数
def create_app(config_name):
    app = Flask(__name__)
    #导入settings配置信息
    app.config.from_object(config[config_name])
    #第三方库初始化
    config_extensions(app)
    #注册所有的蓝本函数
    config_blueprint(app)
    #错误页面绑定app
    errors(app)
    return app

def errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/error.html',error=e)

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('errors/error.html', error=e)
