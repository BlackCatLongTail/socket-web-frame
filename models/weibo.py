from models import Model
from models.comment import Comment
from utils import log


class Weibo(Model):
    """
    微博类
    """
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        w = Weibo(form)
        w.user_id = user_id
        w.save()

    @classmethod
    def delete(cls, weibo_id):
        w = Weibo.find_by(id=weibo_id)
        cs = Comment.find_all(weibo_id=w.id)
        log('weibo_delete', cs)
        for c in cs:
            Comment.delete(c.id)

        super().delete(weibo_id)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        w = Weibo.find_by(id=weibo_id)
        w.content = form['content']
        w.save()

    def comments(self):
        cs = Comment.find_all(weibo_id=self.id)
        return cs
