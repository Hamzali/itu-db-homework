"""
Study Group endpoints.
"""
import json
from flask import request

from server import app

from models.setupdb import studygroup_model, student_studygroup_model, student_model, student_course_model

from middlewares import auth_func
from utils import int_to_datetime
from errors import DataBaseException

private_route = auth_func(student_model)


def check_study_group(student, groupid):
    """
    Checks for if the study group is belongs to the current student.
    """
    group = studygroup_model.find_by_id(_id=groupid)
    if group:
        if student != group[0]["created_by"]:
            return "studygroup is not yours", 401
    else:
        return "no studygroup found", 404


@app.route("/studygroups", methods=["GET", "POST"])
@private_route
def list_studygroups(student):
    """
    lists and creates studygroups
    """
    student_courses = student_course_model.find_student_courses(studentid=student["id"])
    student_courses = [r["crn"] for r in student_courses]
    if request.method == "GET":
        try:
            result = studygroup_model.get_available_study_groups(
                student["id"], student_courses, student["study_start"], student["study_end"])
            return json.dumps(result)
        except DataBaseException:
            return "no suitable studygroup", 404
    elif request.method == "POST":
        req_body = request.get_json()
        study_date = int_to_datetime(req_body.get("study_date"))
        if req_body.get("course") not in student_courses:
            result = {}
            result["message"] = "You do not have this course"
            return json.dumps(result), 403
        try:
            studygroup_model.create(data={
                "course": req_body.get("course"),
                "created_by": student["id"],
                "name": req_body.get("name"),
                "description": req_body.get("description"),
                "study_date": study_date,
                "duration": req_body.get("duration")
            })
            result = studygroup_model.find(query="created_by='{}'".format(student["id"]), sort_by="id DESC")[0]
            result["message"] = "created"
            return json.dumps(result)
        except DataBaseException as db_error:
            return db_error.message, 404


@app.route("/studygroups/<groupid>", methods=["GET", "PUT", "DELETE"])
@private_route
def find_update_studygroup(student, groupid):
    """
    With given id parameter updates, deletes or finds the studygroup.
    """
    groupid = int(groupid)
    result = check_study_group(student["id"], groupid)
    if result:
        return result

    if request.method == "GET":
        group = studygroup_model.find_by_id(_id=groupid)[0]
        return json.dumps(group)

    elif request.method == "PUT":
        print("put method")
        req_body = request.get_json()

        data = {}

        if req_body.get("name"):
            data["name"] = req_body.get("name")
        if req_body.get("description"):
            data["description"] = req_body.get("description")

        if req_body.get("study_date"):
            data["study_date"] = int_to_datetime(req_body.get("study_date"))
        if req_body.get("duration"):
            data["duration"] = req_body.get("duration")
        if req_body.get("course"):
            data["course"] = req_body.get("course")

        try:
            result = studygroup_model.update_by_id(_id=groupid, data=data, return_cols=["id"])
            result["message"] = "updated"
            return json.dumps(result)
        except DataBaseException as db_error:
            return db_error.message, 404
    elif request.method == "DELETE":
        try:
            result = studygroup_model.delete_by_id(_id=groupid, return_cols=["id"])
            result["message"] = "studygroup is deleted."
            return json.dumps(result)
        except DataBaseException:
            return "failed to delete study group.", 404


@app.route("/studygroups/students/<studentid>")
@private_route
def find_studygroups_of_student(student, studentid):
    """
    Finds all the study groups of a student participated.
    """
    if student["id"] == studentid:
        return json.dumps(student_studygroup_model.list_studygroups_of_student(studentid=student["id"]))
    else:
        return "this is not yours"

@app.route("/studygroups/<groupid>/students")
@private_route
def list_studygroup_students(student, groupid):
    """
    Lists all the students of the studygroup with the given id.
    """
    groupid = int(groupid)
    result = check_study_group(student["id"], groupid)
    if result:
        return result
    result = student_studygroup_model.list_studygroup_students(studygroupid=groupid)
    return json.dumps(result)


@app.route("/studygroups/<groupid>/students/<studentid>/status", methods=["POST"])
@private_route
def set_student_studygroup_status(student, groupid, studentid):
    """
    Updates the group status of a student in the studygroup with the given id.
    """
    groupid = int(groupid)
    result = check_study_group(student["id"], groupid)
    if result:
        return result

    if request.method == "POST":
        req_body = request.get_json()
        if req_body.status in [0, 1, 2]:
            try:
                result = student_studygroup_model.set_student_status(
                    groupid, studentid, req_body.status)
                result["message"] = "status updated"
                return json.dumps(result)
            except DataBaseException:
                return "failed to update status", 404
