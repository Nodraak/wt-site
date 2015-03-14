
from datetime import datetime

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
    # u'dependencies': [u'flask', u'json', u'db'], ==>> osef
    is_Write = db.Column(db.Boolean)

    def __init__(self, data={}):
        self.branch = data.get('branch', 'None')
        self.language = data.get('language', 'None')
        self.lines = data.get('lines', -1)
        self.project = data.get('project', 'None')
        self.file = data.get('file', 'None')
        self.timestamp = data.get('timestamp', -1)
        self.is_Write = data.get('is_Write', False)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    method = db.Column(db.String(16))
    data = db.Column(db.String(1024))
    datetime = db.Column(db.DateTime(timezone=True))
    # back relation then relation
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'))
    log = db.relationship("Log", backref=db.backref("url", uselist=False))

    def __init__(self, url='None', method='None', data={}):
        self.url = url
        self.method = method
        self.data = str(data)
        self.datetime = datetime.utcnow()

        self.log = Log(data)
        db.session.add(self.log)
