import json

import requests
from flask import request

from constants import MOBIL_ITU_AUTH_URL

from server import app

from models.setupdb import student_model, course_model, student_course_model, student_studygroup_model

from middlewares import auth_func

private_route = auth_func(student_model)


@app.route("/students", methods=["GET", "POST"])
@private_route
def get_students(student):
    """
    GET request Fetches all the students. <br/>
    POST request creates a student.
    """
    if request.method == "GET":
        result = student_model.find()
        if len(result) > 0:
            for r in result:
                r["created_at"] = r["created_at"].isoformat()
        return json.dumps(result)
    elif request.method == "POST":
        req_body = request.get_json()
        return student_model.create(data=req_body)

@app.route("/students/courses/<courseid>", methods=["POST"])
@private_route
def enroll_course(student, courseid):
    if request.method == "POST":
        if course_model.course_exists(courseid):
            try:
                student_course_model.create(data={
                    "student": student["id"],
                    "course": int(courseid)
                })
                return "course is added to student"
            except:
                return "you are already enrolled", 403
        else:
            return "course does not exists", 404
        
@app.route("/students/studygroups/<studygroupid>", methods=["POST"])
@private_route
def join_study_group(student, studygroupid):
    student_studygroup_model.create(data={
        "student":student["id"],
        "studygroup": studygroupid
    })
    return "created"

@app.route("/students/<sid>", methods=["GET", "PUT"])
@private_route
def one_student(student, sid):
    """
    :param student: current logged in student
    :param sid: student id.
    :return: None
    """
    if request.method == "GET":
        if sid == student["id"]:
            result = student
        else:
            result = student_model.find_by_id(_id=sid)
            if len(result) <= 0:
                return "no student found with id %s" % sid
        return json.dumps(result)
    elif request.method == "PUT":
        req_body = request.get_json()
        data = {}
        # add fields to update.
        try:
            updated_id = student_model.update_by_id(_id=sid, data=data)
            updated_keys = []
            for key in data:
                updated_keys.append(key)
            return "{} fields are updated for {}".format(str.join(", ", updated_keys), updated_id)
        except:
            return "error not updated", 404



@app.route("/auth", methods=["POST"])
def student_login():
    if request.method == "POST":
        # Send request to itu mobil api.
        req_body = request.get_json()
        url = MOBIL_ITU_AUTH_URL % (
            req_body["username"], req_body["password"], req_body["pin"])
        r = requests.post(url)
        # Fail if the result is not available.
        if r.status_code is not 200:
            return "login fail!", 401
        # Parse the response.
        r = r.json()["Session"]
        # Try to update the student token.
        res = student_model.update(
            query=("id='%s'" % str(r["ITUNumber"])), 
            data={"token": str(r["Token"])})
        # If it fails create new student.
        if len(res) == 0:
            student_model.create(data={
                "id": str(r["ITUNumber"]),
                "name": r["FirstName"] + " " + r["LastName"],
                "username": r["UserName"],
                "email": r["ITUMail"],
                "faculty": None,
                "token": r["Token"]
            })
        # Send the token to the user.
        return json.dumps({"token": r["Token"]})


@app.route("/logout", methods=["POST"])
def student_logout():
    req_body = request.get_json()
    student_model.remove_token(token=req_body["token"])
    return "logged out"
