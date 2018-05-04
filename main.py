from flask import Flask, render_template, request, session, url_for, redirect, jsonify, flash
from psycopg2 import sql
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from static.python.helpers import hash_password,check_password, today_date, validate_args_exist, DecimalEncoder, dates_to_array
import pymysql.cursors
import json

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='!!',
    variable_end_string='!!'
  ))
  
app = CustomFlask(__name__, static_folder = "./dist/static", template_folder = "./dist")

cors = CORS(app)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airplanes',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

###
#with app.app_context():
#    flight_num = "01010"#rec['flight_num']
#    query = "SELECT * FROM flight natural join ticket where ticket_id NOT IN (SELECT ticket_id FROM ticket natural join purchases) and flight_num = %s"
#    args = (flight_num)
#    cursor = conn.cursor()
#    try:
#        cursor.execute(query, args)
#    except Exception as e:
#        print(e)
#   data = cursor.fetchall()
#### 

@app.route('/api/getflights', methods=['GET', 'POST'])
def get_flights():
    rec = request.json
    cursor = conn.cursor()
    if (rec['date']):
        query = "SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_time between %s and %s"
        try:
            cursor.execute(query, (rec['depart'], rec['arrive'], rec['date'], rec['date']+' 23:59:59'))
        except:
            return json.dumps({"success":"false", "message": "database query failed"})
    else:
        query = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s'
        cursor.execute(query, (rec['depart'], rec['arrive']))
    ret = cursor.fetchall()
    return json.dumps(ret,default=str)

@app.route('/api/createflight', methods=['GET', 'POST'])
def create_flight():
    global rec
    rec = request.json
    for r in rec:
        if not rec[r]:
            return json.dumps({"success":"false", "message": "please submit all of the required fields"})
    cursor = conn.cursor()
    query = "insert into flight values(%s,%s, %s, %s, %s, %s, %s, %s, %s)"
    args = (rec['airline_name'],rec['flight_num'],rec['departure_airport'],rec['date1']+' '+rec['time1'],
             rec['arrival_airport'],rec['date2']+' '+rec['time2'],rec['price'],rec['flight_status'],rec['airplane_id'])
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    
    return json.dumps({"success":"true", "message": "Flight inserted successfully"})

@app.route('/api/changeflightstatus', methods=['GET','POST'])
def change_flight_status():
    pass

@app.route('/api/addairplane', methods=['GET','POST'])
def add_airplane():
    pass

@app.route('/api/addairport', methods=['GET','POST'])
def add_airport():
    pass

@app.route('/register/auth', methods = ['GET', 'POST'])
def registerAuth():
    global rec
    rec = request.json
    cursor = conn.cursor()
    if rec['typ'] == "customer":
        query = 'SELECT * FROM customer WHERE email = %s'
    elif rec['typ'] == "booking_agent":
        query = 'SELECT * FROM booking_agent WHERE email = %s'
    else:
        query = 'SELECT * FROM airline_staff WHERE username = %s'
    args = (rec['email'],)
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchone()
    if data:
        return json.dumps({"success":"false", "message":"This user already exists in the database"})  
    
    #Else, not in database so proceed with insertion
    hashed_pass = hash_password(rec['password'])
    if rec['typ'] == "customer":
        query = 'insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        args = (rec['email'], rec['name'],hashed_pass,rec['building_number'], rec['street'],rec['city'],rec['state'],
                rec['phone_number'],rec['passport_number'],rec['passport_expiration'],rec['passport_country'],rec['dob'])
    elif rec['typ'] == "airline_staff":
        query = 'insert into airline_staff values(%s,%s,%s,%s,%s,%s)'
        args = (rec['email'], hashed_pass, rec['first_name'], rec['last_name'], rec['dob'], rec['airline_name'])
    elif rec['typ'] == "booking_agent":
        query = 'insert into booking_agent values(%s,%s,%s)'
        args = (rec['email'], hashed_pass, rec['booking_agent_id'])
    for a in args:
            if not a:
                print(args)
                return json.dumps({"success":"false", "message": "please submit all of the required fields"})
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message":"database insertion failed"})
    return json.dumps({"success":"true", "message":"Registration successfull"})    

@app.route('/login/auth', methods=['GET', 'POST'])
def loginAuth():
    rec = request.json
    username = rec['email']
    password = rec['password']
    login = 'false'
    message = "login successful"
    cursor = conn.cursor()
    typ = rec['typ']
    
    if typ == "customer":
        query = 'SELECT email,password FROM customer WHERE email = %s'
    elif typ == "airline_staff":
        query = 'SELECT * FROM airline_staff WHERE username = %s'
    elif typ == "booking_agent":
        query = 'SELECT * FROM booking_agent WHERE email = %s'
    try:
        cursor.execute(query, (username))
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    
    data = cursor.fetchone()
    if(data and check_password(data['password'], password)):
        session['username'] = username
        session['role'] = rec['typ']
        print("username:",session['username'])
        session.modified = True;
        login = "true"
        message = "login successful"
    elif data:
        message = "incorrect email/password combination"
        login = "false"
    else:
        message = "user not found"
        login = "false"
    print(cursor._last_executed)
    cursor.close()
    return json.dumps({"success" : login, "message" : message, "username":rec['email'], "role":rec['typ']})

@app.route('/session/vars', methods=['GET', 'POST'])
def send_session_vars():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    if "role" in session:
        role = session["role"]
    else:
        role = ""
    return json.dumps({"username":username, "role":role})

@app.route('/api/customerspending', methods = ['GET','POST'])
def get_customer_spending():
#    if "username" not in session:
#        return json.dumps({"success":"false", "message": "You must be logged in"})
    rec = request.json
    username = "colton@nyu" #session['username']
    date1 = "2017-01-03"#rec['date1']
    date2 = "2018-06-01"#rec['date2']
    cursor = conn.cursor()
    query = 'SELECT sum(price) as sump, YEAR(purchase_date) as year, MONTH(purchase_date) as month FROM `purchases` natural join `ticket` natural join flight where customer_email = %s and purchase_date BETWEEN %s and %s GROUP BY YEAR(purchase_date), MONTH(purchase_date);'
    args = (username, date1, date2)
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    global data
    data = cursor.fetchall()
    labels,vals = dates_to_array(date1, date2)
    if data:
        for d in data:
            d['sump'] = float(d['sump'])
            date = str(d['year']) + '-' + "%02d"%d['month']
            print(date)
            i = labels.index(date)
            vals[i] = d['sump']
            
    return json.dumps({"success":"true", "message": "Query succeeded", "labels" :labels, "vals": vals},cls = DecimalEncoder)



@app.route('/purchase/ticket', methods = ['GET', 'POST'])
def buy_ticket():
    #check if tickets are available
    global rec
    rec = request.json
    flight_num = rec['flight_num']
    print(session.keys())
    if "username" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in before you can make a purchase"})
    query = "SELECT * FROM flight natural join ticket where ticket_id NOT IN (SELECT ticket_id FROM ticket natural join purchases) and flight_num = %s"
    args = (flight_num)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchall()
    if not data:
        return json.dumps({"success":"false", "message": "Sorry, we're sold out of tickets"})
    ## fetch one of those ticket ids and purchase it
    ticket_id = data[0]['ticket_id']
    if session['role'] == 'customer':
        query = "insert into purchases values(%s,%s, NULL, %s)"
        args = (ticket_id,session["username"], today_date())
    elif session['role'] == 'booking_agent':
        query = 'insert into purchases values(%s, %s, %s, %s)'
        args = (ticket_id,rec['customer_username'],  session['username'], today_date())
    else:
        return json.dumps({"success":"false", "message": "Please make purchase as either a booking agent or customer"})
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database insertion failed"})
    
    return json.dumps({"success":"true", "message": "Ticket purchased!"})

@app.route('/logout/auth', methods=['GET', 'POST'])
def logout():
    if "username" in session:
        session.pop("username")
    if "role" in session:
        session.pop("role")
    return json.dumps({"success":"true", "message": "You are logged out"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html", username = "colton")
    #here's where you left off
    

if __name__ == "__main__":
    app.secret_key = "I gotta s3cret key that youll never know"
    app.run('127.0.0.1', 5000, use_debugger = True)
    