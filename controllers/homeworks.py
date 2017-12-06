import json
import requests
from flask import request
from server import app, auto
from models.homeworks import homeworks, hwOnSt


@app.route('/homeworks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def homework():
    if request.method == 'GET':
        # TODO: get students id somehow?
        return json.dumps(hwOnSt.showHomeworks(data={student_id: "150140124"}))
    
    elif request.method == 'POST':
        data = request.get_json()
        homeworks.addHomework(data)
        return json.dumps(hwOnSt.addHomeworkOfStudent(data))
    
    elif request.method == 'PUT':
        data = request.get_json()
        return json.dumps(homeworks.changeHomework(data))
    
    elif request.method == 'DELETE':
        data = request.get_json()
        return json.dumps(hwOnSt.removeStudentsHomework(data))

