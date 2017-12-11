import json
import requests
from flask import request
from server import app
from models.setupdb import student_model, homeworks, hwOnSt
from middlewares import auth_func

private_route = auth_func(student_model)


@app.route('/api/homeworks', methods=['GET', 'POST', 'PUT', 'DELETE'])
@private_route
def homework(student):

    if request.method == 'GET':
        return json.dumps(hwOnSt.showHomeworks(data=student["id"]))
    
    elif request.method == 'POST':

        data = request.get_json()
        data.update({"created_by": student["id"]})
        homeworks.addHomework(data)
        lastHomeworkCreatedBy = str((homeworks.getLastHwCreatedById(
                                    data=data["created_by"])[0])["id"])

        hwOnSt.addHomeworkOfStudent({"student_id": student["id"],
                                     "homework_id": lastHomeworkCreatedBy})
        return json.dumps(hwOnSt.showHomeworks(data=student["id"]))
    
    elif request.method == 'PUT':
        data = request.get_json()
        hwid = data["homework_id"]
        del data["homework_id"]
        
        return json.dumps(homeworks.changeHomework(hwid=hwid, data=data))
    
    elif request.method == 'DELETE':
        data = request.get_json()
        data["sid"] = student["id"]
        # return json.dumps(data)
        hwOnSt.removeStudentsHomework(data=data)
        return "Success", 200
    
    else:
        return "Wrong request", 301

