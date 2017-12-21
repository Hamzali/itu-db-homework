import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from server import app
from models.setupdb import commentsTable, student_model
from middlewares import auth_func

private_route = auth_func(student_model)

@app.route("/api/comments", methods=['GET', 'POST', 'DELETE'])
@private_route
def comments(student):
    """
    POST request will add comment to student\n
    DELETE request will remove the comment
    """

    if request.method == 'POST':
        data = request.get_json()
        data["comment_by"] = student["id"]
        commentsTable.addComment(data)
        return "Success", 200

    elif request.method == 'DELETE':
        data = request.get_json()
        commentsTable.removeComment(data)
        return "Success", 200


@app.route("/api/comments/<sid>", methods=['GET'])
def getCommentsOfStudent(sid):
    """
        Returns a JSON containing comments of specific student
    """
    if request.method == 'GET':
        data = {"comment_to": sid}
        return json.dumps(commentsTable.showCommentsOfStudent(data))