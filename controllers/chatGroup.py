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
        data = "4"
        return json.dumps(studentsOnChat.showGroupsOfStudent(data=data))
    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup(data)
        return json.dumps(studentsOnChat.addMember(data))


@app.route("/chatgroup/<cid>", methods=['GET', 'PUT', 'DELETE'])
#
def students_group(cid):
    """
    GET request will show the group to student
    PUT request will add student to chatgroup.
    DELETE request will remove student from chat.
    """
    if request.method == 'GET':
        # TODO: add students id as well
        data = {"cid": cid}
        checkIfMember = studentsOnChat.listMembersOfGroup(data)
        return json.dumps(studentsOnChat.listMembersOfGroup(data=data))

    elif request.method == 'PUT':
        data = request.get_json()
        return studentsOnChat.addMember(data)

    elif request.method == 'DELETE':
        data = request.get_json()
        isAdminRes = chatGroups.checkIsAdmin(data)

        if cid in isAdminRes:
            return studentsOnChat.removeMember(data)

        else:
            return "You can't not remove people when you are not admin!",404
