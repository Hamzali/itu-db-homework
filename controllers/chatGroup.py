import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app
from models.setupdb import student_model, chatGroups, studentsOnChat


@app.route("/chatgroup", methods=['GET', 'POST'])
# @auth_func(student_model)
def show_groups():
    """
    GET request show all the groups of student. <br/>
    POST request allows student to form a group.
    """
    if request.method == 'GET':

        try:
            token = str(request.headers["token"])
        except:
            return "Please provide token", 401

        student = student_model.validate_token(token)
        
        if len(student) <= 0:
            return "Invalid access", 403

        return json.dumps(studentsOnChat.showGroupsOfStudent(data=student[0]["id"]))

    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup(data)
        lastGroupCreatedBy = str((chatGroups.getLastGroupCreatedById(data=data["created_by"])[0])["id"])
        
        
                  
        # return json.dumps(newdat)
        studentsOnChat.addMember({"chatgroup_id": lastGroupCreatedBy,
                                  "student_id": data["created_by"]})
        return "Success", 200


@app.route("/chatgroup/<cid>", methods=['GET', 'PUT', 'DELETE'])
def students_group(cid):
    """
    GET request will show the group to student
    PUT request will add student to chatgroup.
    DELETE request will remove student from chat.
    """

    try:
        return str(chatGroups.listGroups()[int(cid) - 1]["id"])

    except:
        return "This group cannot be found in database!", 404

    if request.method == 'GET':
        try:
            token = str(request.headers["token"])

        except:
            return "Please provide token", 401

        student = student_model.validate_token(token)
        data = {"cid": cid, "sid": student[0]["id"]}
        checkIfMember = studentsOnChat.listMembersOfGroup(data)
        return json.dumps(studentsOnChat.listMembersOfGroup(data=data))

    elif request.method == 'PUT':
        data = request.get_json()
        newData = {"chatgroup_id": cid, "student_id": data["student_id"]}
        return studentsOnChat.addMember(newData)

    elif request.method == 'DELETE':
        data = request.get_json()
        isAdminRes = chatGroups.checkIsAdmin(data)

        # TODO: What happens if admin removes himself from group?

        if cid in isAdminRes:
            return studentsOnChat.removeMember(data)

        else:
            return "You can't not remove people when you are not admin!", 404


@app.route("/chatgroup/<cid>/leave", methods=["GET"])
def leave_chatgroup(cid):


    if request.method == 'GET':
        try:
            token = str(request.headers["token"])

        except:
            return "Please provide token", 401

    student = student_model.validate_token(token)
    data = {"cid": str(cid), "sid": str(student[0]["id"])}
    checkIfMember = studentsOnChat.listMembersOfGroup(data)

    if student[0]["id"] == checkIfMember[0]["student_id"]:
        studentsOnChat.removeMember(data)
        return "Success", 200

    else:
        return "Do not try to harm the balance of nature!", 404
