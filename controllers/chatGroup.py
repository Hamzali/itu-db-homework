import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app
from models.setupdb import student_model, chatGroups, studentsOnChat

private_route = auth_func(student_model)


@app.route("/api/chatgroup", methods=['GET', 'POST'])
@private_route
def show_groups(student):
    """
    GET request show all the groups of student. <br/>
    POST request allows student to form a group.
    """
    if request.method == 'GET':
        return json.dumps(studentsOnChat.showGroupsOfStudent(data=student["id"]))

    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup({"group_admin": student["id"],
                                "name": data["name"],
                                "created_by": student["id"]})
        
        lastGroupCreatedBy = str(chatGroups.getLastGroupCreatedById(data=student["id"])[0]["id"])
        studentsOnChat.addMember({"chatgroup_id": lastGroupCreatedBy,
                                  "student_id": student["id"]})

        return json.dumps(studentsOnChat.showGroupsOfStudent(data=student["id"]))


@app.route("/chatgroup/<cid>", methods=['GET', 'PUT', 'DELETE'])
@private_route
def students_group(student, cid):
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
        data = {"cid": cid, "sid": student["id"]}
        checkIfMember = studentsOnChat.listMembersOfGroup(data)
        return json.dumps(studentsOnChat.listMembersOfGroup(data=data))

    elif request.method == 'PUT':
        data = request.get_json()
        newData = {"chatgroup_id": cid, "student_id": data["student_id"]}
        return studentsOnChat.addMember(newData)

    elif request.method == 'DELETE':
        data = request.get_json()
        isAdminRes = chatGroups.checkIsAdmin(data)

        if cid in isAdminRes:
            return studentsOnChat.removeMember(data)

        else:
            return "You can't not remove people when you are not admin!", 404


@app.route("/chatgroup/<cid>/leave", methods=["GET"])
@private_route
def leave_chatgroup(cid):

    data = {"cid": str(cid), "sid": str(student["id"])}
    checkIfMember = studentsOnChat.listMembersOfGroup(data)

    if student["id"] == checkIfMember[0]["student_id"]:
        studentsOnChat.removeMember(data)
        return "Success", 200

    else:
        return "Do not try to harm the balance of nature!", 404
