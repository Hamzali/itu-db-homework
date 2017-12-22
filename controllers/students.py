import json

import requests
from flask import request

from constants import MOBIL_ITU_AUTH_URL

from server import app

from models.setupdb import student_model, course_model, student_course_model, student_studygroup_model, studygroup_model

from middlewares import auth_func
from utils import int_to_datetime
from errors import DataBaseException

private_route = auth_func(student_model)


@app.route("/students", methods=["GET", "PUT"])
@private_route
def one_student(student):
    """
    :param student: current logged in student from auth decorator.
    
    | route: /students
    | method: GET
    | Retrieves one student with id.

    | route: /students
    | method: PUT
    | body: {"study_start": [timestamp], "study_end": [timestamp]}
    | Updates one student study time preference with id.
    """
    if request.method == "GET":        
        return json.dumps(student)
    elif request.method == "PUT":
        req_body = request.get_json()
        data = {}
        if req_body.get("study_start"):
            data["study_start"] = int_to_datetime(req_body.get("study_start"))
        if req_body.get("study_end"):
            data["study_end"] = int_to_datetime(req_body.get("study_end"))
        
        student["id"] = "'{}'".format(student["id"])
        updated_keys = []
        for key in data:
            updated_keys.append(key)
        try:
            result = student_model.update_by_id(_id=student["id"], data=data, return_cols=["id"] + updated_keys)
            result["message"] = "student is updated."
            return json.dumps(result)
        except DataBaseException as db_error:
            result = {}
            result["message"] = "error not updated"
            result["error"] = db_error.message
            return json.dumps(result), 404
        except Exception as e:
            print(e)
            return "something is wrong", 500


@app.route("/auth", methods=["POST"])
def student_login():
    """
    | route: /auth
    | method: POST
    | body: {"username": [string], "password": [string], "pin": [string]}
    | Makes authentication with ITU username, password and pin number.
    """
    if request.method == "POST":
        # Send request to itu mobil api.
        req_body = request.get_json()
        print(req_body)
        url = MOBIL_ITU_AUTH_URL % (
            req_body.get("username"),
            req_body.get("password"),
            req_body.get("pin"))
        try:
            result = requests.post(url)
            print(result)
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
            return "login failed, try again!", 404
        except:
            return "something went wrong", 500


@app.route("/logout", methods=["POST"])
def student_logout():
    """
    | route: /logout
    | method: POST
    | Logs out the logged in user.
    """
    try:
        student_model.remove_token(token=request.headers["token"])
        return "logged out!"
    except DataBaseException:
        return "could not log out!", 500


@app.route("/students/courses")
@private_route
def list_student_courses(student):
    """
    :param student: current logged in student from auth decorator.

    | route: /students/courses
    | method: GET
    | Lists all the courses of a student.
    """
    try:
        result = student_course_model.find_student_courses(studentid=student["id"])
        return json.dumps(result)
    except DataBaseException:
        return "no course found lazy boy", 404


@app.route("/students/courses/<courseid>", methods=["POST", "DELETE"])
@private_route
def enroll_course(student, courseid):
    """
    :param student: current logged in student from auth decorator.

    | route: /students/courses/<crn>
    | method: POST
    | Enrolls a course with given CRN.

    | route: /students/courses/<crn>
    | method: DELETE
    | Leaves a course with given CRN.
    """
    courseid = int(courseid)
    course = course_model.course_exists(courseid)
    if course:
        if request.method == "POST":
            try:
                student_course_model.create(data={
                    "student": student["id"],
                    "course": courseid
                })
                return json.dumps(course)
            except DataBaseException:
                return "you are already enrolled", 403
        elif request.method == "DELETE":
            try:
                student_course_model.delete_student_course(
                    student["id"], courseid)
                return json.dumps(course)
            except DataBaseException as db_error:
                print(db_error)
                return "could not be deleted!", 404
    else:
        return "course does not exists", 404


@app.route("/students/studygroups")
@private_route
def list_student_studygroups(student):
    """
    :param student: current logged in student from auth decorator.

    | route: /students/studygroups
    | method: GET
    | List all the created study groups.
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
    :param student: current logged in student from auth decorator.

    | route: /students/studygroups/<studygroupid>
    | method: GET
    | Joins a study group.
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
