from datetime import datetime

from test.app import db, app


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<news {}>'.format(self.topic)


db.create_all()
print("what")

news = News(id=1, topic="1", url="1", time=datetime.now())
db.session.add(news)
db.session.commit()

if __name__ == '__main__':
    app.run()
