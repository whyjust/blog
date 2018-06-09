from App.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
#生成token的模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from flask import current_app
from flask_login import UserMixin
from App.extensions import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12),index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Boolean,default=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(40))
    icon = db.Column(db.String(70),default='default.jpg')
    #当期账户激活状态
    confirm = db.Column(db.Boolean,default=False)

    @property
    def password(self):
        raise ValueError

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #生成token的方法
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id})

    #检测token的方法
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        # print(s)
        #从当前的token中拿出字典
        try:
            id = s.loads(token)['id']
        except:
            return False

        u = User.query.get(id)

        if not u:
            return False
        if not u.confirm:
            print(u.confirm)
            u.confirm = True
            print(u.confirm)
            db.session.add(u)
        return True


    #验证密码
    def check_password_hash(self,password):
        return check_password_hash(self.password_hash,password)

#登录认证的回调  保持数据的一致性
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))