from flask import Flask
from config import *

from models import init_models

from controllers.students import *
from controllers.courses import *
from controllers.studygroups import *

from middlewares import auth_func

app = Flask(__name__)

appSettings = os.environ.get("APP_SETTINGS")
app.config.from_object(appSettings)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


Models = init_models(app)

private_route = auth_func(Models["student"])


@app.after_request
def after_all_requests(response):
    # Parse to json or format here.
    return response


@app.route("/")
def root_path_handler():
    return "This is for the test!"


init_student_controller(
    app, Models["student"], Models["course"], Models["student_course"], Models["student_studygroup"], private_route)
init_course_controller(
    app, Models["course"], Models["building"], Models["faculty"], Models["course_building"])

init_studygroup_controller(app, Models["studygroup"], Models["student_studygroup"], private_route)

port = int(os.getenv("PORT", "5000"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
