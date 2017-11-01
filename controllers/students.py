from server import app
from models.students import *
import requests
import json

from flask import request
from constants import MOBIL_ITU_AUTH_URL
init_student_table()


@app.route('/students', methods=['GET', 'POST'])
def get_students():
    if request.method == 'GET':
        return json.dumps(list_students())
    elif request.method == 'POST':
        req_body = request.get_json()
        return create_student(data=req_body)


@app.route('/students/<sid>', methods=['GET', 'PUT'])
def one_student(sid):
    if request.method == 'GET':
        result = find_one_student_by_id(_id=sid)
        if len(result) <= 0:
            return 'no student found with id %s' % sid
        return json.dumps(result)
    elif request.method == 'PUT':
        req_body = request.get_json()
        return update_student(_id=sid, data=req_body)


@app.route('/auth', methods=['POST'])
def student_login():
    # TODO: Create sessions and make auth.
    if request.method == 'POST':
        req_body = request.get_json()
        url = MOBIL_ITU_AUTH_URL % (req_body['username'], req_body['password'], req_body['pin'])
        r = requests.post(url)

        # TODO: Create student if it does not exists in the database.

        if r.status_code is not 200:
            return 'login fail!'
        r = r.json()

        return update_student(_id=r['Session']['ITUNumber'], data={'token': r['Session']['Token']})


@app.route('/logout', methods=['POST'])
def student_logout():
    req_body = request.get_json()
    remove_token(token=req_body['token'])