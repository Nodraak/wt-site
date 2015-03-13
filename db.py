
from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    method = db.Column(db.String(16))
    data = db.Column(db.String(1024))
    datetime = db.Column(db.DateTime(timezone=True))

    def __init__(self, url):
        self.url = url
        self.datetime = datetime.utcnow()

