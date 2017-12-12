import re
import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app
from models.setupdb import lecturers


@app.route('/api/lecturers', methods=['GET', 'POST', 'DELETE', 'PUT'])
def lecturer():
    
    """
    GET request shows lecturers of given department
    POST request creates new lecturer
    DELETE request deletes a lecturer
    PUT request updates the lecturer
    """
    # Works on frontend
    if request.method == 'GET':
        
        try:
            dep = (request.args["dep"])
            app.logger.debug(app)
            return json.dumps(lecturers.listLecturersOfDepartment(data=dep))

        except:
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
        lecturers.removeLecturer(data=data)
        try:
            dep = (request.args["dep"])
            return json.dumps(lecturers.listLecturersOfDepartment(data=dep))

        except:
            return "Please give proper department", 200

    elif request.method == 'PUT':
        data = request.get_json()
        json.dumps(lecturers.updateLecturer(data))
        try:
            dep = (request.args["dep"])
            return json.dumps(lecturers.listLecturersOfDepartment(data=dep))

        except:
            return "Please give proper department", 200


@app.route('/api/lecturers/<lid>', methods=['GET'])
def show_a_lecturer(lid):

    if request.method == 'GET':
        return json.dumps(lecturers.showALecturer(data={'id': lid}))
