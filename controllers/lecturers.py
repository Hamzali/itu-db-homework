import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app, auto
from models.lecturers import lecturers
import re


@app.route('/lecturers', methods=['GET', 'POST', 'DELETE', 'PUT'])
def lecturer():
    """
    GET request shows lecturers of given department
    POST request creates new lecturer
    DELETE request deletes a lecturer
    PUT request updates the lecturer
    """
    
    if request.method == 'GET':
        dep = str(request.headers["dep"])
        
        if dep is not None or len(dep) > 0:
            lecturers.listLecturersOfDepartment(dep)
            return "Success", 200
        
        else:
            return "Please give proper department", 404

    elif request.method == 'POST':
        data = request.get_json()
        isEmailExists = data.get("email", -1)

        if isEmailExists == -1:
            return "Please provide email address!"
        
        if not re.match("[^@]+@[^@]+\.[^@]+", data['email']):
            return "Invalid email address!", 404
        
        lecturers.addLecturer(data)
        return "Success", 200

    elif request.method == 'DELETE':
        data = request.get_json()
        return json.dumps(lecturers.removeLecturer(data))

    elif request.method == 'PUT':
        data = request.get_json()
        return json.dumps(lecturers.updateLecturer(data))


@app.route('/lecturers/<lid>', methods=['GET'])
def show_a_lecturer(lid):

    if request.method == 'GET':
        return json.dumps(lecturers.showALecturer(data={'id': lid}))
