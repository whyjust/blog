from app.models import User
from flask import Blueprint,render_template,flash,url_for,redirect,current_app
from app.forms import Register,Login,Icon
from app.extensions import db,file,cache
from app.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user
import os
from PIL import Image

user = Blueprint('user',__name__)

#注册
@user.route('/register/',methods=['GET','POST'])
def register():
    #实例化form
    form = Register()
    if form.validate_on_submit():
        # 实例化user模型类
        u = User(username=form.username.data,password=form.password.data,email=form.email.data)

        db.session.add(u)
        db.session.commit()
        # 生成token
        token = u.generate_token()
        send_mail('邮件激活',form.email.data,'activate',username=form.username.data,token=token)
        #提示用户注册信息
        flash('注册成功请去邮箱中激活')
        #跳转到登陆页面
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)

#激活
@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('激活成功请登录')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))

#登录
@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        # print(u.username)
        if not u:
            flash('该用户不存在')
        elif not u.confirm:
            flash('该用户没有激活')
        elif u.check_password_hash(form.password.data):
            # print('231')
            flash('登录成功')
            cache.clear()
            login_user(u,remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的密码')
    return render_template('user/login.html',form=form)

#登出
@user.route('/logout/')
def logout():
    cache.clear()
    logout_user()
    flash('退出成功！')
    return redirect(url_for('main.index'))
#生成新的名字
def new_name(shuffix,length=32):
    import string,random
    myStr = string.ascii_letters+'0123456789'
    return ''.join(random.choice(myStr) for i in range(length)) + shuffix




#修改头像
@user.route('/change_icon/',methods=['GET','POST'])
def change_icon():
    form = Icon()
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        #生成随机图片

        while True:
            newName = new_name(shuffix)
            if not os.path.exists(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName)):
                break
        file.save(form.file.data,name=newName)
        print(current_user.icon)

        if current_user.icon != 'default.jpg':
            # print('11313')
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))

        # 执行缩放
        img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], newName))
        img.thumbnail((300, 300))
        # 保存新的图片名称为新的图片的newname
        img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],  newName))

        current_user.email = form.email.data

        current_user.icon = newName
        db.session.add(current_user)
        flash('头像上传成功')



    img_url = file.url(current_user.icon)
    # print(img_url)
    return render_template('user/change_icon.html',form=form,img_url=img_url)
