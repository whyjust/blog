from flask import Blueprint,render_template,current_app,request,redirect,url_for
from app.models import Posts,User
from app.extensions import cache

main = Blueprint('main',__name__)

@main.route('/')
#缓存存活时间
def index():
    return redirect(url_for('main.page_show',page=1))

#设置缓存记忆
@cache.memoize(timeout=100)
@main.route('/page_show/<int:page>')
# @cache.cached(timeout=100,key_prefix='index')
def page_show(page):
    #返回按时间倒叙的当前页数的帖子数据
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'], False)
    # 返回当前page的所有数据
    data = pagination.items
    return render_template('main/index.html',data=data,pagination=pagination)

@main.route('/test1/')
def test1():
    u = User.query.get(1)
    p = Posts.query.get(1)
    # id1用户收藏1号帖子
    u.favorite.append(p)

    # 查看用户1收藏了那些帖子
    print(u.favorite.all())

    # 1号帖子被哪些用户 收藏了
    # print(p.users.all())

    # 取消收藏
    # u.favorite.remove(p)
    return 'test'