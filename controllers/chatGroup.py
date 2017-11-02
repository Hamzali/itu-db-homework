from server import app
from models.chatGroup import *
import requests
import json

from flask import request

init_chatGroup_table()

@app.route('/chatgroup', methods=['GET', 'POST'])
def show_groups():
    if request.method == 'GET':
        return json.dumps(list_chatRooms())
    elif request.method == 'POST':
        req_body = request.get_json()
        return create_chatgroup(admin_id=req_body)


#
#@app.route('/chatgroup/<gid>', methods=['GET'])
        