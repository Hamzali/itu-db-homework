import json
import requests
from flask import request
from constants import MOBIL_ITU_AUTH_URL
from server import app
from models.setupdb import commentsTable, student_model
from middlewares import auth_func

private_route = auth_func(student_model)
@app.route("/comments", methods=['GET', 'POST',
                                 'PUT', 'DELETE'])
@private_route                                 
def comments(student):
    """
    GET request will show comments of student
    POST request will add comment to student
    PUT request will update the comment
    DELETE request will remove the comment
    """
    if request.method == 'GET':
        
        data = {"comment_to": student["id"]}
        return json.dumps(commentsTable.showCommentsOfStudent(data))

    elif request.method == 'POST':
        data = request.get_json()
        return json.dumps(commentsTable.addComment(data))

    elif request.method == 'PUT':
        data = request.get_json()
        return json.dumps(commentsTable.updateComment(data))

    elif request.method == 'DELETE':
        data = request.get_json()
        return(json.dumps(commentsTable.removeComment(data)))
