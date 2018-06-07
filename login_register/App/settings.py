import os
#所有环境配置的基类
class Config:
    SECRET_KEY = 'xiafsadwsda'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER =  os.environ.get('MAIL_SERVER','smtp.163.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','15858017847@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','mm22kk11')

#测试配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20111673@127.0.0.1:3306/testing'

#开发配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20111673@127.0.0.1:3306/blogModel'

#生产配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2011673@127.0.0.1:3306/development'
#一个配置的字典
config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'test':TestingConfig,
    'default':DevelopmentConfig
}
