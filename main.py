
import json
from flask import Flask, request
from db import db, Url

app = Flask(__name__)

@app.route('/')
def index():
    all = Url.query.all()

    row_inc = ['</td><td>'.join([str(i.datetime), i.url, i.method, i.data]) for i in all]
    row = ['<td>' + s + '</td>' for s in row_inc]
    body_inc = '</tr>\n<tr>'.join(row)
    body = '<tr>' + body_inc + '</tr>'
    head_inc = '</th><th>'.join(['date', 'url', 'method', 'data'])
    head = '<tr><th>' + head_inc + '</th></tr>'
    table = '<table>' + head + body + '</table>'

    return '\n'.join((
        '<!DOCTYPE html>',
        '<html>',
            '<head>',
                '<meta charset="utf-8" />',
            '</head>',
            '<body>',
                table,
            '</body>',
        '</html>'
    ))


@app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def other(path):
    tmp = Url(path)
    tmp.method = request.method
    tmp.data = 'None'
    print request
    if request.method == 'POST':
        tmp.data = ','.join([j for j in ':'.join([(i[0], i[1]) for i in request.form.items()])])

    db.session.add(tmp)
    db.session.commit()
    return index()

if __name__ == "__main__":
    app.run(debug=True)

