import json
import requests
from flask import request
from server import app
from models.setupdb import student_model, homeworks, hwOnSt


@app.route('/api/homeworks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def homework():
    # try:
    #         token = str(request.headers["token"])
    
    # except:
    #     return "Please provide token", 401
    
    # student = student_model.validate_token(token)
    student = [{"id": "150140124"}]
    if request.method == 'GET':
        return json.dumps(hwOnSt.showHomeworks(data=student[0]["id"]))
    
    elif request.method == 'POST':

        data = request.get_json()
        data.update({"created_by": student[0]["id"]})
        homeworks.addHomework(data)
        lastHomeworkCreatedBy = str((homeworks.getLastHwCreatedById(
                                    data=data["created_by"])[0])["id"])

        hwOnSt.addHomeworkOfStudent({"student_id": student[0]["id"],
                                     "homework_id": lastHomeworkCreatedBy})
        return "Success", 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        return json.dumps(homeworks.changeHomework(data))
    
    elif request.method == 'DELETE':
        data = request.get_json()
        return json.dumps(hwOnSt.removeStudentsHomework(data))


        
