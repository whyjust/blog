from flask_bootstrap import  Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
#处理用户登录模块
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,patch_request_class,configure_uploads
from flask_moment import Moment
from flask_cache import Cache


#实例化db
db = SQLAlchemy()
#实例化bootstrap
bootstrap = Bootstrap()
#实例化migrate
migrate = Migrate(db=db)
#实例化邮箱
mail = Mail()
#实例化用户登录模块
login_manager = LoginManager()
#实例化文件对象
file = UploadSet('photos',IMAGES)
moment = Moment()
#simple简单缓存
# cache = Cache(config={'CACHE_TYPE':'simple'})
cache = Cache(config={'CACHE_TYPE': 'simple'})

def config_extensions(app):
    #bootstrap初始化app
    bootstrap.init_app(app)
    #db初始化app
    db.init_app(app)
    #migrate初始化app
    migrate.init_app(app=app)
    #mail初始化
    mail.init_app(app)
    #登录模块初始化
    login_manager.init_app(app)
    #moment时间模块初始化
    moment.init_app(app)
    cache.init_app(app=app)



    #需要指定登录端点
    login_manager.login_view ='user.login'
    #提示信息
    login_manager.login_message = '请登录再访问'
    #设置session保护级别
    login_manager.session_protection = 'strong'

    #配置文件上传
    configure_uploads(app,file)
    patch_request_class(app,size=None)
