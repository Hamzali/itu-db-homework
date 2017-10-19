from server import app, db
from models.students import *
import json


@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = db.engine.connect()
    res = conn.execute('select url from results')
    conn.close()
   #
    return json.dumps([dict(r) for r in res])