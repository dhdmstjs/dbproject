#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_cors import CORS
import pymysql.cursors
import json
from bson import json_util

#Initialize the app from Flask
#Change the delimiters to be compatible with flask
class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='!!',
    variable_end_string='!!'
  ))
app = Flask(__name__)

#Cross Origin Resource Sharing
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airplanes',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/api/getflights', methods=['GET', 'POST'])
def get_flights():
    rec = request.json
    cursor = conn.cursor()
    if (rec['date']):
        query = "SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_time between %s and %s"
        cursor.execute(query, (rec['depart'], rec['arrive'], rec['date'], rec['date']+' 23:59:59'))
    else:
        query = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s'
        cursor.execute(query, (rec['depart'], rec['arrive']))
    ret = cursor.fetchall()
    return json.dumps(ret,default=str)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, use_debugger = True)