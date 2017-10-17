import os
from flask import Flask
import psycopg2

from controllers.students import studentsController

app = Flask(__name__)
appSettings = os.environ['APP_SETTINGS']
app.config.from_object(appSettings)
os.

@app.route('/')
def WelcomeToMyapp():
    return 'This is for the test!'


conn = psycopg2.connect(host="104.236.17.86", port="5432",
                        user="hamzali", password="1954lotr", database="testdb")

# Bind controllers.
studentsController(app, conn)

port = int(os.getenv('PORT', '5000'))
print(appSettings, port)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
