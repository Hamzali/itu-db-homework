import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
appSettings = os.environ['APP_SETTINGS']
app.config.from_object(appSettings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def WelcomeToMyapp():
    return 'This is for the test!'


# Bind controllers.
from controllers.students import *

port = int(os.getenv('PORT', '5000'))

print(appSettings, port)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
