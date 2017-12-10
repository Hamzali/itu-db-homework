import os
from flask import Flask

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

appSettings = os.environ.get("APP_SETTINGS")
app.config.from_object(appSettings)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.after_request
def after_all_requests(response):
    # Parse to json or format here.
    return response


@app.route("/")
def root_path_handler():
    return "This is for the test!"

from controllers.students import *
from controllers.courses import *
from controllers.studygroups import *
from controllers.lecturers import *
from controllers.homeworks import *
from controllers.chatGroup import *
from controllers.comments import *


port = int(os.getenv("PORT", "5000"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
