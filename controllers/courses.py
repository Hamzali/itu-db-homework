import json

# import requests
# from flask import request
# from middlewares import private_route
from server import app
from models.courses import course_model


@app.route('/courses')
def list_courses():
	result = course_model.find(return_cols=["id", "name"])
	if result is None or len(result) <= 0:
		return "no courses found.", 404
	return json.dumps(result)


@app.route('/courses/<cid>')
def list_one_course(cid):
	result = course_model.find_by_id(_id=cid)
	if len(result) <= 0:
		return 'no course found with id %s.' % cid, 404
	return json.dumps(result)


# TODO: sync courses endpoint with admin privileges
