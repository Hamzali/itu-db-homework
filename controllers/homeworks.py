import json
import requests
from flask import request
from server import app
from models.setupdb import student_model, homeworks, hwOnSt


@app.route('/homeworks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def homework():
    if request.method == 'GET':
        try:
            token = str(request.headers["token"])
        except:
            return "Please provide token", 401
        student = student_model.validate_token(token)

        return json.dumps(hwOnSt.showHomeworks(data=student[0]["id"]))
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            token = str(request.headers["token"])
        except:
            return "Please provide token", 401
        homeworks.addHomework(data)
        student = student_model.validate_token(token)
        lastHomeworkCreatedBy = str((homeworks.getLastGroupCreatedById(data=data["created_by"])[0])["id"])
        hwOnSt.addHomeworkOfStudent({"student_id": data["student_id"],
                                     "homework_id": lastHomeworkCreatedBy})
        return json.dumps(hwOnSt.addHomeworkOfStudent(data))
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        return json.dumps(homeworks.changeHomework(data))
    
    elif request.method == 'DELETE':
        data = request.get_json()
        return json.dumps(hwOnSt.removeStudentsHomework(data))

