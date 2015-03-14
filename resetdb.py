
import os
from db import db

os.system('rm db.sqlite3')
db.create_all()
