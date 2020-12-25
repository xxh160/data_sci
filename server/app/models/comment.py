from app.db import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return '<content {}>'.format(self.content)
