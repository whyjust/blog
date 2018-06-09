import os
base_path = os.path.abspath(os.path.dirname(__file__))
#配置所有环境的基类
class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '15858017847@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'mm22kk11')

    #配置上传文件
    MAX_CONTENT_LENGTH = 1024*1024*64
    UPLOADED_PHOTOS_DEST = os.path.join(base_path,'static/upload')

    PAGE_NUM = 3
    

#测试
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20111673@127.0.0.1:3306/blog'
#开发
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20111673@127.0.0.1:3306/blog'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_path,'develop.sqlite')
#生产
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20111673@127.0.0.1:3306/blog'

#设置字典
config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'test':TestingConfig,
    'default':DevelopmentConfig
}
