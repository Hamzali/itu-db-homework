import json

import requests
from flask import request

from constants import MOBIL_ITU_AUTH_URL

from server import app

from models.setupdb import student_model, course_model, student_course_model, student_studygroup_model, studygroup_model

from middlewares import auth_func
from utils import jstime_to_datetime
from errors import DataBaseException

private_route = auth_func(student_model)


# @app.route("/students", methods=["GET", "POST"])
# @private_route
# def get_students(student):
#     """
#     GET request Fetches all the students
#     POST request creates a student.
#     """
#     if request.method == "GET":
#         try:
#             result = student_model.find()
#             return json.dumps(result)
#         except DataBaseException:
#             return "nothing found go away", 404
#     elif request.method == "POST":
#         req_body = request.get_json()
#         return student_model.create(data=req_body)


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
        if req_body.get("study_start"):
            data["study_start"] = jstime_to_datetime(
                req_body.get("study_start"))
        if req_body.get("study_end"):
            data["study_end"] = jstime_to_datetime(req_body.get("study_end"))
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
    """
    Makes authentication with ITU username, password and pin number.
    """
    if request.method == "POST":
        # Send request to itu mobil api.
        req_body = request.get_json()
        url = MOBIL_ITU_AUTH_URL % (
            req_body["username"],
            req_body["password"],
            req_body["pin"])
        try:
            result = requests.post(url)
        except requests.exceptions.RequestException as req_exc:
            print(req_exc)
            return "auth service is not available right now", 500
        # Fail if the result is not available.
        if result.status_code is not 200:
            return "login failed, check credentials!", 401
        # Parse the response.
        result = result.json()["Session"]
        # Try to update the student token.
        try:
            token = student_model.update(
                query=("id='%s'" % str(result["ITUNumber"])),
                data={"token": str(result["Token"])}, return_cols=["token"])
            # If it fails create new student.
            if not token:
                student_model.create(data={
                    "id": str(result["ITUNumber"]),
                    "name": result["FirstName"] + " " + result["LastName"],
                    "username": result["UserName"],
                    "email": result["ITUMail"],
                    "faculty": None,
                    "token": result["Token"]
                })
            # Send the token to the user.
            return json.dumps({"token": result["Token"]})
        except DataBaseException:
            return "login failed, try again!"


@app.route("/logout", methods=["POST"])
def student_logout():
    """
    Logs out the logged in user.
    """
    req_body = request.get_json()
    try:
        student_model.remove_token(token=req_body["token"])
        return "logged out!"
    except DataBaseException:
        return "could not log out!", 500


@app.route("/students/courses")
@private_route
def list_student_courses(student):
    """
    Lists all the courses of a student.
    """
    try:
        result = student_course_model.find_student_courses(student["id"])
        return json.dumps(result)
    except DataBaseException:
        return "no course found lazy boy", 404


@app.route("/students/courses/<courseid>", methods=["POST", "DELETE"])
@private_route
def enroll_course(student, courseid):
    """
    Enrolls or leaves a course with given CRN.
    """
    courseid = int(courseid)
    if course_model.course_exists(courseid):
        if request.method == "POST":
            try:
                student_course_model.create(data={
                    "student": student["id"],
                    "course": courseid
                })
                return "course is added to student"
            except DataBaseException:
                return "you are already enrolled", 403
        elif request.method == "DELETE":
            try:
                student_course_model.delete_student_course(
                    student["id"], courseid)
                return "course removed!"
            except DataBaseException as db_error:
                print(db_error)
                return "could not be deleted!", 404
    else:
        return "course does not exists", 404


@app.route("/students/studygroups")
@private_route
def list_student_studygroups(student):
    """
    List all the created study groups.
    """
    try:
        result = student_studygroup_model.find_student_studygroups(
            student["id"])
        return json.dumps(result)
    except DataBaseException:
        return "no studygroup found lazy boy", 404


@app.route("/students/studygroups/<studygroupid>", methods=["POST"])
@private_route
def join_study_group(student, studygroupid):
    """
    Joins a study group.
    """
    try:
        group = studygroup_model.find_by_id(_id=int(studygroupid))
        if group:
            group = group[0]
            if group["created_by"] == student["id"]:
                return "this group created by you can not join to dis!", 403
            else:
                student_studygroup_model.create(data={
                    "student": student["id"],
                    "studygroup": studygroupid
                })
        return "joined studygroup"
    except DataBaseException:
        return "failed to join studygroup", 404
