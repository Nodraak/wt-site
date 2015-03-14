
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(256))
    language = db.Column(db.String(256))
    lines = db.Column(db.Integer)
    project = db.Column(db.String(256))
    file = db.Column(db.String(256))
    timestamp = db.Column(db.Integer)
    is_write = db.Column(db.Boolean)
    other = db.Column(db.Text)

    def __init__(self, data={}):
        self.branch = data.pop('branch', '')
        self.language = data.pop('language', '')
        self.lines = data.pop('lines', 0)
        self.project = data.pop('project', '')
        self.file = data.pop('file', '')
        self.timestamp = int(data.pop('time', 0))
        self.is_write = bool(data.pop('is_write', False))
        self.other = str(data)
