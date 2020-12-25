from app.db import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<news {}>'.format(self.topic)
