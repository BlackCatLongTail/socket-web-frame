from models import Model
from models.user import User
# from models.weibo import Weibo(这样会导致循环导入，不可取)
# model中的依赖关系是：comment -> weibo -> user, comment -> user,这样能避免循环导入。


class Comment(Model):
    """
    评论类
    """
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    @classmethod
    def add(cls, form, user_id, weibo_id):
        c = Comment(form)
        c.user_id = user_id
        c.weibo_id = weibo_id
        c.save()
        return c

    @classmethod
    def update(cls, form):
        comment_id = int(form['id'])
        c = Comment.find_by(id=comment_id)
        c.content = form['content']
        c.save()

