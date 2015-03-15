
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from api import app, db
from api.models import Log

admin = Admin(app)
admin.add_view(ModelView(Log, db.session))


if __name__ == "__main__":
    app.run(debug=True)
