from server import app
from models.chatGroup import *
import requests
import json

from flask import request

init_chatGroup_table()
init_studentsOnChat_table()


@app.route('/chatgroup', methods=['GET', 'POST'])
def show_all_groups():
    if request.method == 'GET':
        return json.dumps(list_chatRooms())
    elif request.method == 'POST':
        req_body = request.get_json()
        return create_chatgroup(admin_id=req_body)

@app.route('/chatgroup/<gid>', methods=['GET', 'PUT'])
@private_route()
def students_group(gid):
    if request.method == 'GET':
        pass
        #return json.dumps(show_groups_of_student)
        # TODO: Parse json and get students' id from request

    elif request.method == 'PUT':
        add_member(conn, gid)

    elif request.method == 'DELETE':
        # TODO: Parse json and get student's id, then remove
        pass
#@app.route('/chatgroup/<gid>', methods=['GET'])
        