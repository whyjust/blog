from flask import Blueprint,render_template,flash,url_for,redirect,jsonify
from app.forms import Posts as PostsForm
from flask_login import current_user
from app.models import Posts
from app.extensions import db

posts = Blueprint('posts',__name__)


#发表帖子的路由,methods一定要记得加上
@posts.route('/send_posts/',methods=['GET','POST'])
def send_posts():
    form = PostsForm()
    #对发表帖子的用户进行验证
    if form.validate_on_submit():
        # print('11')
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            flash('帖子发表成功')
            return redirect(url_for('main.index'))
        else:
            flash('您还没有登录,请登录之后在发表')
            return redirect(url_for('user.login'))
    return render_template('posts/send_posts.html',form=form)

#收藏取消收藏
@posts.route('/favorite/<pid>')
def favorite(pid):
    try:
        if current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
        else:
            current_user.add_favorite(pid)
        return jsonify({'res':200})
    except:
        return jsonify({'res': 500})

