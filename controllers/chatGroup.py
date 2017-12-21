import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from middlewares import auth_func
from server import app
from models.setupdb import student_model, chatGroups, studentsOnChat

private_route = auth_func(student_model)


@app.route("/api/chatgroups", methods=['GET', 'POST'])
@private_route
def show_groups(student):
    """
    GET request show all the groups of student. \n
    POST request allows student to form a group. Returns the new list of student's groups
    """
    # Works
    if request.method == 'GET':
        return json.dumps(studentsOnChat.showGroupsOfStudent(data=student["id"]))
    # Works
    elif request.method == 'POST':
        data = request.get_json()
        chatGroups.createGroup({"group_admin": student["id"],
                                "name": data["name"],
                                "created_by": student["id"]})
        
        lastGroupCreatedBy = str(chatGroups.getLastGroupCreatedById(data=student["id"])[0]["id"])
        studentsOnChat.addMember({"chatgroup_id": lastGroupCreatedBy,
                                  "student_id": student["id"]})

        return json.dumps(studentsOnChat.showGroupsOfStudent(data=student["id"]))


@app.route("/api/chatgroups/<cid>", methods=['GET', 'PUT', 'DELETE'])
@private_route
def students_group(student, cid):
    """
    GET request will show the group to student\n
    PUT request will add student to chatgroup. Returns a JSON object of members of group including the new one.\n
    DELETE request will remove student from chat. Returns a JSON object of members of group excluding the new one.
    """

    try:
        print(str(chatGroups.listGroups()[int(cid) - 1]["id"]))

    except:
        return "This group cannot be found in database!", 404

    if request.method == 'GET':
        data = {"cid": cid, "sid": student["id"]}
        checkIfMember = studentsOnChat.listMembersOfGroup(data)
        return json.dumps(studentsOnChat.listMembersOfGroup(data=data))

    elif request.method == 'PUT':
        newData = {"chatgroup_id": cid, "student_id": str(student["id"])}    
        studentsOnChat.addMember(newData)
        return "Success", 200

    elif request.method == 'DELETE':
        
        newData = {"cid": int(cid), "sid": str(student["id"])}
        isAdminRes = chatGroups.checkIsAdmin(data=newData)

        if isAdminRes[0]["id"] == int(cid):
            studentsOnChat.removeMember(newData)
            return "Success", 200

        return "You can't not remove people when you are not admin!", 404


@app.route("/chatgroups/<cid>/leave", methods=["GET"])
@private_route
def leave_chatgroup(cid):
    """
        Leave room endpoint 
    """
    data = {"cid": str(cid), "sid": str(student["id"])}
    checkIfMember = studentsOnChat.listMembersOfGroup(data)

    if student["id"] == checkIfMember[0]["student_id"]:
        studentsOnChat.removeMember(data)
        return "Success", 200

    else:
        return "Do not try to harm the balance of nature!", 404
