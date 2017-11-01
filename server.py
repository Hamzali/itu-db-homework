import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
appSettings = os.environ['APP_SETTINGS']
app.config.from_object(appSettings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO: Write tests if you can.

@app.before_request
def before_all_requests():
    # Check for auth and other details.
    # print('before a request', request.headers)
    pass


@app.after_request
def after_all_requests(response):
    # Parse to json or format here.
    return response


@app.route('/')
def root_path_handler():
    return 'This is for the test!'


# Bind controllers.
# TODO: Find a clever way to implement the router attachments to Server.
from controllers.students import *

port = int(os.getenv('PORT', '5000'))

print(appSettings, port)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
