import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app, auto
from models.chatGroup import chatGroups, studentsOnChat
from models.students import student_model


@app.route("/chatgroup", methods=['GET', 'POST'])
# @auth_func(student_model)
def show_groups():
    """
    GET request show all the groups of student. <br/>
    POST request allows student to form a group.
    """
    if request.method == 'GET':
        # data = request.get_json()
        # return json.dumps(studentOnChat.showGroupsOfStudent(data=data))
        # TODO: student id is req.
        return json.dumps(chatGroups.find())
    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup(data)
        return json.dumps(studentsOnChat.addMember(data))


@app.route("/chatgroup/<cid>", methods=['GET', 'PUT', 'DELETE'])
# @private.route()
def students_group(cid):
    """
    GET request will show the group to student
    PUT request will add student to chatgroup.
    DELETE request will remove student from chat.
    """
    if request.method == 'GET':
        data = {"cid": cid}
        return json.dumps(studentsOnChat.listMembersOfGroup(data=data))
    elif request.method == 'PUT':
        data = request.get_json()
        return studentsOnChat.addMember(data)

    elif request.method == 'DELETE':
        data = request.get_json()
        return studentsOnChat.removeMember(data)

