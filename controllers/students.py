import json

import requests
from flask import request

from constants import MOBIL_ITU_AUTH_URL
from middlewares import private_route
from models.students import *
from server import app

init_student_table()


@app.route('/students', methods=['GET', 'POST'])
def get_students():
    if request.method == 'GET':
        return json.dumps(list_students())
    elif request.method == 'POST':
        req_body = request.get_json()
        return create_student(data=req_body)


@app.route('/students/<sid>', methods=['GET', 'PUT'])
@private_route()
def one_student(student, sid):
    if request.method == 'GET':
        if sid == student['id']:
            result = student
        else:
            result = find_one_student_by_id(sid=sid)
            if len(result) <= 0:
                return 'no student found with id %s' % sid
        return json.dumps(result)
    elif request.method == 'PUT':
        req_body = request.get_json()
        return update_student(sid=sid, data=req_body)


@app.route('/auth', methods=['POST'])
def student_login():
    if request.method == 'POST':
        # Send request to itu mobil api.
        req_body = request.get_json()
        url = MOBIL_ITU_AUTH_URL % (req_body['username'], req_body['password'], req_body['pin'])
        r = requests.post(url)
        # Fail if the result is not available.
        if r.status_code is not 200:
            return 'login fail!'
        # Parse the response.
        r = r.json()['Session']
        # Try to update the student token.
        res = update_student(sid=str(r['ITUNumber']), data={'token': r['Token']})
        # If it fails create new student.
        if len(res) == 0:
            create_student({
                'id': str(r['ITUNumber']),
                'name': r['FirstName'] + ' ' + r['LastName'],
                'username': r['UserName'],
                'email': r['ITUMail'],
                'faculty': None,
                'token': r['Token']
            })
        # Send the token to the user.
        return json.dumps({'token': r['Token']})


@app.route('/logout', methods=['POST'])
def student_logout():
    req_body = request.get_json()
    remove_token(token=req_body['token'])
