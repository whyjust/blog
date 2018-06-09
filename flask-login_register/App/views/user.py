from flask import Blueprint,render_template,flash,redirect,url_for
from App.models import User
from App.forms import Register,Login
from App.extensions import db
from App.email import send_mail
from flask_login import login_user,logout_user,current_user



user = Blueprint('user',__name__)

#注册
@user.route('/register/',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        #实例化user模型类
        u = User(username=form.username.data,password=form.password.data,email=form.email.data)
        db.session.add(u)
        db.session.commit()
        #生成token
        token = u.generate_token()
        #发送邮件
        send_mail('邮件激活',form.email.data,'activate', username=form.username.data,token=token)
        #提示用户注册称该
        flash('注册成功请去邮箱中激活')
        #跳转到登录页面
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)

@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('激活成功 请登录')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


#登录
#加一个时间的验证  如果输入错误超过三次  把激活改为False
@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('该用户不存在')
        elif not u.confirm:
            flash('该用户还没激活！！！')
        elif u.check_password_hash(form.password.data):
            flash('登录成功！')
            login_user(u,remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的密码')
    return render_template('user/login.html',form=form)

#退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('退出成功！')
    return redirect(url_for('main.index'))

