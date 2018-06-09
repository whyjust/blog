from app.extensions import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
#生成token的模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from flask_login import UserMixin
from flask import current_app
from .posts import Posts

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column(db.String(12),index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Boolean,default=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(40))
    icon = db.Column(db.String(70),default='default.jpg')
    #当期账户激活状态
    confirm = db.Column(db.Boolean,default=False)
    #参数1模型名称   参数2反向引用的字段名   参数3 加载方式 提供对象
    posts = db.relationship('Posts',backref='user',lazy='dynamic')
    #secondary在多对多关系中指定关联表的名称
    favorite = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')
    #添加使用append   删除使用remove

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
        #从当前的token中拿出字典
        try:
            id = s.loads(token)['id']
        except:
            return False
        #根据用户id取出对应用户的对象
        u = User.query.get(id)
        #判断 当期u对象是否存在
        if not u:
            return False
        #判断当期用户的激活状态 如果没有激活 则激活
        if not u.confirm:
            u.confirm = True
            db.session.add(u)
        return True
    #验证密码
    def check_password_hash(self,password):
        return check_password_hash(self.password_hash,password)


    def is_favorite(self,postsId):
        all = self.favorite.all()
        for p in all:
            if p.id==postsId:
                return True
            #lambda表达式
            if list(filter(lambda p:p.id==int(postsId),all)):
                return True
            return False

    #定义一个收藏与取消收藏方法
    def add_favorite(self,pid):
        self.favorite.append(Posts.query.get(pid))

    #定义一个取消收藏方法
    def remove_favorite(self,pid):
        self.favorite.remove(Posts.query.get(pid))





#登录认证的回调,保持数据的一致性
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))