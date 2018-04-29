from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_cors import CORS
from static.python.helpers import hash_password,check_password
import pymysql.cursors
import json

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='!!',
    variable_end_string='!!'
  ))
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airplanes',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

###
#with app.app_context():
#    cursor = conn.cursor()
#    query = 'insert into customer values("colton@nyu","colton","password","test","test","test","test","test","test","2020-04-01","test","1996-02-09")'
#    cursor.execute(query)
#    conn.commit()
#### 

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

@app.route('/register/auth', methods = ['GET', 'POST'])
def registerAuth():
    rec = request.json
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s'
    try:
        cursor.execute(query, (rec['email']))
    except Exception as e:
        print(e)
        return json.dumps({"register":"false", "message": "database operation failed"})
    data = cursor.fetchone()
    if data:
        return json.dumps({"register":"false", "message":"This user already exists in the database"})  
    query = 'insert into customer values("%s","%s",%s,"test","test","test","test","test","test","2020-04-01","test","1996-02-09")'
    hashed_pass = hash_password(rec['password'])
    cursor = conn.cursor()
    try:
        cursor.execute(query, (rec['email'], rec['name'], hashed_pass))
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"register":"false", "message":"database operation failed"})
    return json.dumps({"register":"true", "message":"Registration successfull"})
    

@app.route('/login/auth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
    global data
    rec = request.json
    username = rec['email']
    password = rec['password']
    login = 'false'
    message = "login successful"
    cursor = conn.cursor()
    #todo: choose query based on radio button
    typ = "customer"
    
    if typ == "customer":
        query = 'SELECT email,password FROM customer WHERE email = "%s"'
    elif typ == "booking_agent":
        query = 'SELECT * FROM airline_staff WHERE username = "%s"'
    else:
        query = 'SELECT * FROM booking_agent WHERE email = "%s"'
    try:
        cursor.execute(query, (username))
    except Exception as e:
        print(e)
        return json.dumps({"login":"false", "message": "database query failed"})
    
    data = cursor.fetchone()
    if(data and check_password(data['password'], password)):
        session['username'] = username
        login = "true"
        message = "login successful"
    elif data:
        message = "incorrect email/password combination"
        login = "false"
    else:
        message = "user not found"
        login = "false"
        
    cursor.close()
    return json.dumps({"login" : login, "message" : message})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = "I gotta s3cret key that youll never know"
    app.run('127.0.0.1', 5000, use_debugger = True)