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
    GET request shows all lecturers
    POST request creates new lecturer
    DELETE request deletes a lecturer
    PUT request updates the lecturer
    """
    
    if request.method == 'GET':
        return json.dumps(lecturers.listAllLecturers())

    elif request.method == 'POST':
        data = request.get_json()
        if not re.match("[^@]+@[^@]+\.[^@]+", data['email']):
            return "Invalid email address!"
        return json.dumps(lecturers.addLecturer(data))

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
