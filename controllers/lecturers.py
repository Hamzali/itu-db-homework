import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import private_route
from server import app, auto
from models.lecturers import lecturers


@app.route('/lecturers', methods=['GET', 'POST', 'DELETE', 'PUT'])
def show_lecturers():
    """
    GET request shows all lecturers
    POST request creates new lecturer
    DELETE request deletes a lecturer
    PUT request updates the lecturer
    """
    data = request.get_json()
    if request.method == 'GET':
        return lecturers.showALecturer(data)

    elif request.method == 'POST':
        return lecturers.addLecturer(data)

    elif request.method == 'DELETE':
        return lecturers.removeLecturer(data)

    elif request.method == 'PUT':
        return lecturers.updateLecturer(data)


@app.route('lecturers/<lid>', methods=['GET'])
def show_a_lecturer(lid):
    
    if request.method == 'GET':
        data = request.get_json()
        return lecturers.showALecturer(data)