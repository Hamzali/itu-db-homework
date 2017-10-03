import os
from flask import Flask, jsonify
import psycopg2

from controllers.students import studentsController

app = Flask(__name__)
appSettings = os.environ['APP_SETTINGS']
app.config.from_object(appSettings)

@app.route('/')
def WelcomeToMyapp():
    return 'This is for the test!'

conn = psycopg2.connect(host="postgres", port="5432", user="marco", password="foobarbaz", database="testdb")

# Bind controllers.
studentsController(app, conn)

port = int(os.getenv('PORT', '5000'))
print(appSettings, port)
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)
