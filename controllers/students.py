import json

import requests
from flask import request

from constants import MOBIL_ITU_AUTH_URL

def init_student_controller(app, student_model, private_route):
    @app.route('/students', methods=['GET', 'POST'])
    def get_students():
        """
        GET request Fetches all the students. <br/>
        POST request creates a student.
        """
        if request.method == 'GET':
            return json.dumps(student_model.find())
        elif request.method == 'POST':
            req_body = request.get_json()
            return student_model.create(data=req_body)


    @app.route('/students/<sid>', methods=['GET', 'PUT'])
    @private_route()
    def one_student(student, sid):
        """
        :param student: current logged in student
        :param sid: student id.
        :return: None
        """
        if request.method == 'GET':
            if sid == student['id']:
                result = student
            else:
                result = student_model.find_by_id(_id=sid)
                if len(result) <= 0:
                    return 'no student found with id %s' % sid
            return json.dumps(result)
        elif request.method == 'PUT':
            req_body = request.get_json()
            return student_model.update_by_id(_id=sid, data=req_body)


    @app.route('/auth', methods=['POST'])
    def student_login():
        if request.method == 'POST':
            # Send request to itu mobil api.
            req_body = request.get_json()
            url = MOBIL_ITU_AUTH_URL % (
                req_body['username'], req_body['password'], req_body['pin'])
            r = requests.post(url)
            # Fail if the result is not available.
            if r.status_code is not 200:
                return 'login fail!', 401
            # Parse the response.
            r = r.json()['Session']
            # Try to update the student token.
            res = student_model.update_by_id(
                str(r["ITUNumber"]), {"token": str(r["Token"])})
            # If it fails create new student.
            if len(res) == 0:
                student_model.create(data={
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
        student_model.remove_token(token=req_body['token'])
