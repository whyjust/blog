from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

#通过函数create_app进行包括蓝本/扩展/系统配置的初始化
app = create_app('default')
manager = Manager(app)
#给manage添加迁移命令db
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
