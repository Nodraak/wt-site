
from datetime import datetime, timedelta
from flask import request
from sqlalchemy.sql import extract
from . import app, db
from .models import Log


@app.route('/')
def index():
    return 'hello world !'


@app.route('/api', methods=['POST'])
def api():
    tmp = Log(request.get_json())
    db.session.add(tmp)
    db.session.commit()

    return index()


@app.route('/time_by_file/<path:path>')
def time_by_file(path):
    path = '/' + path
    logs = Log.query.filter_by(file=path).order_by(Log.date.desc()).all()

    time = 0
    for i in xrange(len(logs)):
        if logs[i].is_write and i+1 != len(logs):
            diff = logs[i].date - logs[i+1].date
            if diff < timedelta(minutes=10):
                time += diff.total_seconds()
                logs[i+1].is_write = True

    return str(time) + '<br>--<br>' + '<br>'.join([str(i) for i in logs])


@app.route('/time_overall')
def time_overall():
    week = 4

    times = []
    for i in range(-week*7+1, 0+1):
        today = datetime.today()

        logs = Log.query.filter(
            (extract('year', Log.date) == today.year) &
            (extract('month', Log.date) == today.month) &
            (extract('day', Log.date) == today.day+i)
        ).order_by(Log.date.desc()).all()

        tmp = 0
        for i in xrange(len(logs)):
            if logs[i].is_write and i+1 != len(logs):
                diff = logs[i].date - logs[i+1].date
                if diff < timedelta(minutes=10):
                    tmp += diff.total_seconds()
                    logs[i+1].is_write = True
        times.append(tmp)

    #time_str = []
    #for time in times:
    #    time_str.append("%02d:%02d:%02d" % (time/3600, (time/60)%60, time % 60))

    #return '<br />'.join(time_str)

    ret_data = zip(times, range(-week*7+1, 0+1))

    ret = """
    <html>
      <head>
        <script type="text/javascript"
              src="https://www.google.com/jsapi?autoload={
                'modules':[{
                  'name':'visualization',
                  'version':'1',
                  'packages':['corechart']
                }]
              }"></script>

        <script type="text/javascript">
          google.setOnLoadCallback(drawChart);

          function drawChart() {
            var data = google.visualization.arrayToDataTable([
              ['Date', 'Secondes'],
              %s
            ]);

            var options = {
              title: 'Time overall',
              curveType: 'function',
              legend: { position: 'bottom' }
            };

            var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="curve_chart" style="width: 900px; height: 500px"></div>
      </body>
    </html>
    """ % '\n'.join(["['%d', %d]," % (time, date) for time, date in ret_data])

    return ret

