
from flask import request
from . import app, db
from .models import Log


@app.route('/')
def index():
    return 'hello world !'


@app.route('/api', methods=['POST'])
def other():
    tmp = Log(request.get_json())
    db.session.add(tmp)
    db.session.commit()

    return index()


@app.route('/file/<path:path>')
def get_time(path):
    logs = Log.query.filter_by(file='/'+path).order_by(Log.timestamp.desc()).all()

    time = 0
    for i in xrange(len(logs)):
        if logs[i].is_write and i+1 != len(logs):
            diff = logs[i].timestamp - logs[i+1].timestamp
            if diff < 60*10:
                time += diff
                logs[i+1].is_write = True

    return str(time) + '<br>--<br>' + '<br>'.join([str(i) for i in logs])
