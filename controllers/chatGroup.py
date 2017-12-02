import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import private_route
from server import app, auto
from models.chatGroup import chatGroups, studentOnChat


@app.route("/chatgroup", methods=['GET', 'POST'])
# @auto.doc()
def show_groups():
    """
    GET request show all the groups of student. <br/>
    POST request allows student to form a group.
    """
    if request.method == 'GET':
        data = request.get_json()
        # return json.dumps(studentOnChat.showGroupsOfStudent(data=data))
        return chatGroups.listGroups()
    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup(data)
        return json.dumps(studentOnChat.addMember(data))


@app.route("/chatgroup/<cid>", methods=['GET', 'PUT', 'DELETE'])
# @private.route()
def students_group(cid):
    """
    GET request will show the group to student
    PUT request will add student to chatgroup.
    DELETE request will remove student from chat.
    """
    if request.method == 'GET':
        data = request.get_json()
        if studentOnChat.checkIfMember(data):
            # Return to chatroom
            return ('/%s' % cid)
        else:
            return "You are not allowed to see this page!"
    
    elif request.method == 'PUT':
        data = request.get_json()
        return studentOnChat.addMember(data)

    elif request.method == 'DELETE':
        data = request.get_json()
        return studentOnChat.removeMember(data)

    

