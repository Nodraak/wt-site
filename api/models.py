
from datetime import datetime
from . import db


class Log(db.Model):  # TODO : rename to heartbeat
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(256))
    language = db.Column(db.String(256))
    lines = db.Column(db.Integer)
    project = db.Column(db.String(256))
    file = db.Column(db.String(256))
    date = db.Column(db.DateTime)
    is_write = db.Column(db.Boolean)
    other = db.Column(db.Text)

    def __init__(self, data={}):
        self.branch = data.pop('branch', '')
        self.language = data.pop('language', '')
        self.lines = data.pop('lines', 0)
        self.project = data.pop('project', '')
        self.file = data.pop('file', '')
        self.date = datetime.fromtimestamp(data.pop('time', 0))
        self.is_write = bool(data.pop('is_write', False))
        self.other = str(data)

    def __repr__(self):
        return str(self.date)
