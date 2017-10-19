from server import app, db
from models.students import *
import json
from flask import request



@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        result = list_students()
        return json.dumps([dict(r) for r in result])
    elif request.method == 'POST':
        req_body = request.get_json(force=True)
        return create_student(req_body)
    
    
    return 'students!'