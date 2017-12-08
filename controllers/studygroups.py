"""
doc string for module
"""
import json
import datetime
from flask import request

def init_studygroup_controller(app, studygroup_model, student_studygroup_model, private_route):
    def check_study_group(student, groupid):
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
        if request.method == "GET":
            # TODO find suitable studygroups for student
            result = studygroup_model.find()
            return json.dumps(result)
        elif request.method == "POST":
            req_body = request.get_json()
            study_date = datetime.datetime.fromtimestamp(req_body.get("study_date") / 1000)
            try:
                studygroup_model.create(data={
                    "course": req_body.get("course"),
                    "created_by": student["id"],
                    "name": req_body.get("name"),
                    "description": req_body.get("description"),
                    "study_date": study_date,
                    "duration": req_body.get("duration")
                })
            except:
                return "could not create do it right bitch", 404

            return "created bitch!"


    @app.route("/studygroups/<groupid>", methods=["GET", "PUT"])
    @private_route
    def find_update_studygroup(student, groupid):
        """
        Finds a studygroup or updates by id.
        """
        groupid = int(groupid)
        result = check_study_group(student["id"], groupid)
        if result:
            return result

        if request.method == "GET":
            group = studygroup_model.find_by_id(_id=groupid)[0]
            group["created_at"] = group["created_at"].isoformat()
            group["study_date"] = group["study_date"].isoformat()
            return json.dumps(group)

        elif request.method == "PUT":
            req_body = request.get_json()

            data = {}
            if req_body.get("study_date"):
                data["study_date"] = req_body.get("study_date")
            if req_body.get("name"):
                data["name"] = req_body.get("name")
            if req_body.get("description"):
                data["description"] = req_body.get("description")
            if req_body.get("study_date"):
                data["study_date"] = req_body.get("study_date")
            if req_body.get("duration"):
                data["duration"] = req_body.get("duration")
            if req_body.get("course"):
                data["course"] = req_body.get("course")

            try:
                studygroup_model.update_by_id(_id=groupid, data=data)
                return "updated!"
            except:
                return "failed", 404
        elif request.method == "DELETE":
            try:
                studygroup_model.delete_by_id(_id=groupid)
                return "deleted!"
            except:
                return "failed", 404

    
    @app.route("/studygroups/<groupid>/students")
    @private_route
    def list_studygroup_students(student, groupid):
        """
        Finds a studygroup or updates by id.
        """
        groupid = int(groupid)
        result = check_study_group(student["id"], groupid)
        if result:
            return result
        result = studygroup_model.list_studygroup_students(_id=groupid)

        return json.dumps(result)
    
    @app.route("/studygroups/<groupid>/students/<studentid>/status", methods=["POST"])
    @private_route
    def set_student_studygroup_status(student, groupid, studentid):
        """
        Finds a studygroup or updates by id.
        """
        groupid = int(groupid)
        result = check_study_group(student["id"], groupid)
        if result:
            return result

        if request.method == "POST":
            req_body = request.get_json()
            result = student_studygroup_model.set_student_status(studentid, req_body.status)
            if result:
                return "updated"
            return "failed"


        
