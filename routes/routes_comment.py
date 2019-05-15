from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    RenderTemplate,
    current_user,
    html_response,
    login_required,
)
from utils import log


def add(request):
    u = current_user(request)
    form = request.form()
    weibo_id = int(form['weibo_id'])

    c = Comment.add(form, u.id, weibo_id)
    log('comment add', c, u, form)

    return redirect('/weibo/index')


def delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')


def edit(request):
    comment_id = int(request.query['id'])
    c = Comment.find_by(id=comment_id)
    body = RenderTemplate.render('comment_edit.html', comment=c)
    return html_response(body)


def update(request):
    form = request.form()
    Comment.update(form)
    return redirect('/weibo/index')


def same_user_required_update(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('same_user_required_update')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.find_by(id=int(comment_id))

        # 只有comment的拥有者可修改
        if c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def same_user_required_delete(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('same_user_required_update')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.find_by(id=int(comment_id))
        w = Weibo.find_by(id=c.weibo_id)

        # comment的拥有者或者comment所属weibo的发布者可删
        if u.id in [c.user_id, w.user_id]:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    d = {
        '/comment/add': login_required(add),
        '/comment/delete': login_required(same_user_required_delete(delete)),
        '/comment/edit': login_required(same_user_required_update(edit)),
        '/comment/update': login_required(same_user_required_update(update))
    }
    return d
