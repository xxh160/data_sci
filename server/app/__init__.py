from flask import Flask

from app import config
from app.db import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()
