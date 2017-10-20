from server import app, db
from models.students import *

from flask import request

init_student_table()


@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        return list_students()
    elif request.method == 'POST':
        req_body = request.get_json(force=True)
        return create_student(data=req_body)
    return 'students!'


@app.route('/students/<sid>', methods=['GET', 'PUT'])
def one_student(sid):
    if request.method == 'GET':
        return find_one_student_by_id(db_id=sid)
    elif request.method == 'PUT':
        req_body = request.get_json(force=True)
        return update_student(db_id=sid, data=req_body)
    return 'student!'
