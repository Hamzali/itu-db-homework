# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/')
def WelcomeToMyapp():
    return 'This is for the test!'

port = os.getenv('PORT', '5000')
debugEnv = os.getenv('FLASK_DEBUG');

debugVal = False;
if int(debugEnv) == 1:
    debugVal = True

if debugVal:
    conn = psycopg2.connect(host="postgres", port="5432", user="marco", password="foobarbaz", database="testdb")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=debugVal)
