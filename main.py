
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from db import db, Url, Log


app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

admin = Admin(app)
admin.add_view(ModelView(Url, db.session))
admin.add_view(ModelView(Log, db.session))


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
    data = request.get_json() if request.method == 'POST' else {}

    url = Url(path, request.method, data)
    db.session.add(url)
    db.session.commit()

    return index()


if __name__ == "__main__":
    app.run(debug=True)
