from flask import Flask, render_template, request, session, url_for, redirect, jsonify, flash
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

@app.route('/api/changeflightstatus', methods=['GET', 'POST'])
def change_flight_status():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    airline = get_airline_staff_airline_name()
    rec = request.json
    for r in rec:
        if not rec[r]:
            return json.dumps({"success":"false", "message": "please submit all of the required fields"})
    args = (rec['flight_status'],airline,rec['flight_num'])
    cursor = conn.cursor()
    conn.commit()
    query = 'UPDATE `flight` SET `status` = %s WHERE `flight`.`airline_name` = %s AND `flight`.`flight_num` = %s;'
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    return json.dumps({"success":"true", "message": "Flight status updated successfully"})

@app.route('/api/createflight', methods=['GET','POST'])
def create_flight():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
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
    return json.dumps({"success":"true", "message": "Flight created successfully"})

@app.route('/api/addairplane', methods=['GET','POST'])
def add_airplane():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    airline = get_airline_staff_airline_name()
    rec = request.json
    for r in rec:
        if not rec[r]:
            return json.dumps({"success":"false", "message": "please submit all of the required fields"})
    cursor = conn.cursor()
    query = 'insert into airplane values(%s, %s, %s)'
    args = (airline, rec['airplane_id'], rec['seats'])
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    return json.dumps({"success":"true", "message": "Airplane created successfully"})

@app.route('/api/addairport', methods=['GET','POST'])
def add_airport():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    rec = request.json
    for r in rec:
        if not rec[r]:
            return json.dumps({"success":"false", "message": "please submit all of the required fields"})
    cursor = conn.cursor()
    query = 'insert into `airport` values(%s, %s);'
    args = (rec['airport_name'], rec['airport_city'])
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    return json.dumps({"success":"true", "message": "Airport created successfully"})

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
    
    session['username'] = rec['email']
    session['role'] = rec['typ']
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
    print(username, role)
    return json.dumps({"username":username, "role":role})

@app.route('/api/customerflights', methods = ['GET', 'POST'])
def get_customer_flights():
    if "username" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in"})
    username = session['username']
    query = 'SELECT airline_name, flight_num, purchase_date, departure_airport, departure_time, arrival_airport, arrival_time, status FROM purchases natural join ticket natural join flight WHERE departure_time > %s and customer_email = %s;'
    args = (today_date(), username)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchall()
    print(data)
    return json.dumps({"success":"true", "message": "query successful", "data" : data}, indent=4,sort_keys=True, default=str)

@app.route('/api/bookingagentflights', methods = ['GET', 'POST'])
def get_booking_agent_flights():
    if "username" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in"})
    username = session['username']
    query = 'SELECT airline_name, flight_num, purchase_date, customer_email, arrival_time, departure_airport, departure_time, arrival_airport, status FROM purchases natural join ticket natural join flight natural join booking_agent WHERE departure_time > %s and booking_agent.email = %s;'
    args = (today_date(), username)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchall()
    print(data)
    print(cursor._last_executed)
    return json.dumps({"success":"true", "message": "query successful", "data" : data}, indent=4,sort_keys=True, default=str)

#requires "date1" and date2" (requires "username" only in the testing stage)
@app.route('/api/customerspending', methods = ['GET','POST'])
def get_customer_spending():
    if "username" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in"})
    rec = request.json
    username = session['username']
    date1 = rec['date1']
    date2 = rec['date2']
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
    s = 0
    for v in vals:
        s+= v

    return json.dumps({"success":"true", "message": "Query succeeded", "labels" :labels, "vals": vals, "total": s},cls = DecimalEncoder)

#requires "date1" and "date2" (requires "username" only during testing stage)
@app.route('/api/bookingagentcommission', methods = ['GET','POST'])
def get_booking_agent_commission():
    global data
    cursor = conn.cursor()
    if "username" not in session or "role" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in for this operation"})
    rec = request.json
    date1 = rec['date1']
    date2 = rec['date2']
    email = session['username']
    query = 'SELECT .10*sum(price) as sump FROM `booking_agent` natural join purchases natural join ticket natural join flight where purchase_date BETWEEN %s and %s and booking_agent.email = %s'
    args = (date1,date2, email)
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    sump = cursor.fetchone()['sump']
    if sump:
        sump = float(sump)
    else:
        sump = 0
    query2 = 'SELECT count(ticket_id) as total_sold FROM `booking_agent` natural join purchases natural join ticket natural join flight where purchase_date BETWEEN %s and %s and booking_agent.email = %s'
    try:
        cursor.execute(query2, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    total_sold = cursor.fetchone()['total_sold']
    if total_sold:
        total_sold = int(total_sold)
    else:
        total_sold = 0
    query3 = 'SELECT .10*sum(price)/count(ticket_id) as avg_ticket_price FROM `booking_agent` natural join purchases natural join ticket natural join flight where purchase_date BETWEEN %s and %s and booking_agent.email = %s'
    try:
        cursor.execute(query3, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    avg_ticket_price = cursor.fetchone()['avg_ticket_price']
    if avg_ticket_price:
        avg_ticket_price = float(avg_ticket_price)
    else:
        avg_ticket_price = 0
    return json.dumps({"success":"true", "message": "Query succeeded, bookingagentcommission", "total_cost":sump, "avg_ticket_price":avg_ticket_price, "total_sold":total_sold})

#requires "username" during the testing phase
@app.route('/api/bookingagenttopcustomers', methods = ['GET', 'POST'])
def get_top_customers():
    cursor = conn.cursor()
    date1 = date2 = today_date()
    email = session['username']
    commission_query = 'SELECT .10*sum(price) as sump, customer_email FROM `booking_agent` natural join purchases natural join ticket natural join flight where booking_agent.email = %s and purchase_date BETWEEN DATE_SUB(%s, INTERVAL 1 YEAR) and %s group by customer_email ORDER BY `sump` DESC limit 5'
    ticket_query = 'SELECT customer_email, count(ticket_id) as count_t FROM `booking_agent` natural join purchases natural join ticket natural join flight where booking_agent.email = %s and purchase_date BETWEEN DATE_SUB(%s, INTERVAL 6 MONTH) and %s group by customer_email ORDER BY count(ticket_id) DESC limit 5'
    args = (email, date1, date2)
    try:
        cursor.execute(ticket_query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    ticket_data = cursor.fetchall()
    try:
        cursor.execute(commission_query, args)
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database query failed"})
    commission_data = cursor.fetchall()
    commission_ret = {"labels":[],"values":[]}
    ticket_ret = {"labels":[],"values":[]}
    
    

    for c in commission_data:
        commission_ret['labels'].append(c['customer_email'])
        commission_ret['values'].append(int(c['sump']))

    for t in ticket_data:
        ticket_ret['labels'].append(t['customer_email'])
        ticket_ret['values'].append(t['count_t'])
        

    return json.dumps({"success":"true", "message":"database query succeeded, bookingagenttopcustomers", "ticket_customers":ticket_ret, "commission_customers":commission_ret, "commission_data":commission_data, "ticket_data":ticket_data}, indent=4,sort_keys=True, default=str)

#requires "flight_num"
#requires "customer_username" if role is booking_agent
@app.route('/purchase/ticket', methods = ['GET', 'POST'])
def buy_ticket():
    #check if tickets are available
    global rec
    rec = request.json
    flight_num = rec['flight_num']
    print(session.keys())
    if "username" not in session:
        return json.dumps({"success":"false", "message": "You must be logged in before you can make a purchase"})
    print(session['username'])
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

def get_airline_staff_airline_name():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    cursor = conn.cursor()
    username = username = session['username']
    query = 'select airline_name from airline_staff where airline_staff.username = %s'
    try:
        cursor.execute(query, (username))
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database insertion failed"})
    airline = cursor.fetchone()['airline_name']
    return airline

@app.route('/api/airlinestaffflights', methods = ['GET', 'POST'])
def get_airline_staff_flights():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    rec = request.json
    cursor = conn.cursor()
    airline = get_airline_staff_airline_name()
    if not rec['date1']:
        date1 = "1900-01-01"
    else:
        date1 = rec['date1']
    if not rec['date2']:
        date2 = "3000-01-01"
    else:
        date2 = rec['date2']
    if rec['arrival_airport'] and rec['departure_airport']:
        query_flights = 'SELECT * FROM flight where airline_name = %s and departure_time between %s and %s and departure_airport = %s and arrival_airport = %s'
        args = (airline, date1, date2+' 23:59:59', rec['departure_airport'], rec['arrival_airport'])
    elif rec['arrival_airport'] and rec['departure_airport']:
        query_flights = 'SELECT * FROM flight where airline_name = %s and departure_time between %s and %s and arrival_airport = %s'
        args = (airline, date1, date2+' 23:59:59', rec['arrival_airport'])
    elif rec['arrival_airport'] and rec['departure_airport']:
        query_flights = 'SELECT * FROM flight where airline_name = %s and departure_time between %s and %s and departure_airport = %s'
        args = (airline, date1, date2+' 23:59:59', rec['departure_airport'])
    else:
        query_flights = 'SELECT * FROM flight where airline_name = %s and departure_time between %s and %s'
        args = (airline, date1, date2+' 23:59:59')
    try:
        cursor.execute(query_flights, (args))
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database insertion failed"})
    data = cursor.fetchall()
    for d in data:
        flight_number = d['flight_num']
        query_customers = 'SELECT customer_email, name, date_of_birth from flight natural join ticket natural join purchases natural join customer where flight_num = %s and purchases.customer_email = customer.email'
        try:
            cursor.execute(query_customers, (flight_number))
            conn.commit()
        except Exception as e:
            print(e)
            print(cursor._last_executed)
            return json.dumps({"success":"false", "message": "database insertion failed"})
        custs = cursor.fetchall()
        d.update( {"customers":custs})
    return json.dumps({"success":"true", "message": "succss, airline staff flights", "flights": data}, indent=4,sort_keys=True, default=str)

@app.route('/api/airlinestaffbookingagents', methods = ['GET', 'POST'])
def get_airline_staff_booking_agents():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    cursor = conn.cursor()
    airline = get_airline_staff_airline_name()
    args = (airline, today_date(), today_date())
    commission_year_query = 'SELECT booking_agent.email, sum(flight.price) * .10 as commission FROM purchases natural join ticket natural join flight, booking_agent where purchases.booking_agent_id = booking_agent.booking_agent_id and flight.airline_name =%s and purchase_date between DATE_SUB(%s, INTERVAL 1 YEAR) and %s group by booking_agent.booking_agent_id order by sum(flight.price) desc limit 5'
    ticket_month_query = 'SELECT booking_agent.email, count(ticket_id) as tickets FROM purchases natural join ticket natural join flight, booking_agent where purchases.booking_agent_id = booking_agent.booking_agent_id and flight.airline_name = %s and purchase_date between DATE_SUB(%s, INTERVAL 1 MONTH) and %s group by booking_agent.booking_agent_id order by count(ticket_id) desc limit 5'
    ticket_year_query = 'SELECT booking_agent.email, count(ticket_id) as tickets FROM purchases natural join ticket natural join flight, booking_agent where purchases.booking_agent_id = booking_agent.booking_agent_id and flight.airline_name = %s and purchase_date between DATE_SUB(%s, INTERVAL 1 YEAR) and %s group by booking_agent.booking_agent_id order by count(ticket_id) desc limit 5'
    try:
        cursor.execute(commission_year_query, args)
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
    com_year_data = cursor.fetchall()
    if com_year_data:
        com_year_data[0]['commission'] = float(com_year_data[0]['commission'])
    try:
        cursor.execute(ticket_month_query, args)
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
    ticket_month_data = cursor.fetchall()
    try:
        cursor.execute(ticket_year_query, args)
        conn.commit()
    except Exception as e:
        print(e)
        print(cursor._last_executed)
        return json.dumps({"success":"false", "message": "database insertion failed"})
    ticket_year_data = cursor.fetchall()
    return json.dumps({"success":"true", "message": "database query successfull, airlinestaffbookingagent", "commission_year_data":com_year_data, "ticket_year_data" : ticket_year_data, "ticket_month_data" : ticket_month_data})

@app.route('/api/bookingagenttopdestinations', methods=['GET', 'POST'])
def get_top_destinations():
    cursor = conn.cursor()
    month_query = 'select airport_city, count(ticket_id) as count_t from airport, flight natural join ticket natural join purchases where airport.airport_name = flight.arrival_airport and flight.departure_time BETWEEN DATE_SUB(%s, INTERVAL 3 MONTH) and %s group by airport_city order by count_t desc limit 3'
    year_query = 'select airport_city, count(ticket_id) as count_t from airport, flight natural join ticket natural join purchases where airport.airport_name = flight.arrival_airport and flight.departure_time BETWEEN DATE_SUB(%s, INTERVAL 1 YEAR) and %s group by airport_city order by count_t desc limit 3'
    date = today_date()
    try:
        cursor.execute(month_query, (date, date))
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    month_data = cursor.fetchall()
    try:
        cursor.execute(year_query, (date, date))
        conn.commit()
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    year_data = cursor.fetchall()
    return json.dumps({"success":"true", "message": "database query successful", "month_destinations": month_data, "year_destinations":year_data})

@app.route('/api/comparerevenue', methods=['GET', 'POST'])
def compare_revenue():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    cursor = conn.cursor()
    airline = get_airline_staff_airline_name()
    date1 = date2 = today_date()
    args = (airline, date1, date2)
    query = 'select sum(price) as sump from purchases natural join ticket natural join flight where airline_name = %s and purchases.booking_agent_id IS NULL and purchases.purchase_date between DATE_SUB(%s, INTERVAL 1 MONTH) and %s '
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
    rev = cursor.fetchone()['sump']
    if rev:
        revenue_from_direct_sales_month = int(rev)
    else:
        revenue_from_direct_sales_month = 0
    query = 'select sum(price)- .10*sum(price) as sump from purchases natural join ticket natural join flight where airline_name = %s and purchases.booking_agent_id IS NOT NULL and purchases.purchase_date between DATE_SUB(%s, INTERVAL 1 MONTH) and %s'
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
    rev = cursor.fetchone()['sump']
    if rev:
        revenue_from_agents_month = int(rev)
    else:
        revenue_from_agents_month = 0
        
    query = 'select sum(price) as sump from purchases natural join ticket natural join flight where airline_name = %s and purchases.booking_agent_id IS NULL and purchases.purchase_date between DATE_SUB(%s, INTERVAL 1 YEAR) and %s'
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
    rev = cursor.fetchone()['sump']
    if rev:
        revenue_from_direct_sales_year = int(rev)
    else:
        revenue_from_direct_sales_year = 0
    query = 'select sum(price)- .10*sum(price) as sump from purchases natural join ticket natural join flight where airline_name = %s and purchases.booking_agent_id IS NOT NULL and purchases.purchase_date between DATE_SUB(%s, INTERVAL 1 YEAR) and %s'
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        print(e)
    rev = cursor.fetchone()['sump']
    if rev:
        revenue_from_agents_year = int(rev)
    else:
        revenue_from_agents_year = 0
    return json.dumps({"success":"true", "message": "database query succeeded", "direct_sales_month":revenue_from_direct_sales_month, "agents_sales_month":revenue_from_agents_month, "direct_sales_year":revenue_from_direct_sales_year, "agent_sales_year":revenue_from_agents_year})

#requires date1 and date2 from frontend
@app.route('/api/viewreports', methods=['GET', 'POST'])
def view_reports():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    rec = request.json
    date1 = rec['date1']
    date2 = rec['date2']
    airline_name = get_airline_staff_airline_name()
    cursor = conn.cursor()
    query = 'SELECT count(ticket.ticket_id) as count_t, YEAR(purchase_date) as year, MONTH(purchase_date) as month from flight natural join ticket natural join purchases where airline_name = %s and purchase_date BETWEEN %s and %s'
    args = (airline_name, date1, date2)
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchall()
    labels,vals = dates_to_array(date1, date2)
    if data:
        for d in data:
            d['count_t'] = int(d['count_t'])
            date = str(d['year']) + '-' + "%02d"%d['month']
            print(date)
            i = labels.index(date)
            vals[i] = d['count_t']   
    s = 0
    for v in vals:
        s+=v
    return json.dumps({"success":"false", "message": "database query, viewreports", "labels":labels, "values":vals, "total":s})

@app.route('/api/viewfrequentcustomers', methods = ['GET', 'POST'])
def view_frequent_customers():
    if 'role' not in session:
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    if session['role'] != "airline_staff":
        return json.dumps({"success":"false", "message": "You do not have permission for this request"})
    cursor = conn.cursor()
    airline_name = get_airline_staff_airline_name()
    date = today_date()
    query = 'SELECT customer.email, count(ticket.ticket_id) as count_t from flight natural join ticket natural join purchases natural join customer where airline_name = %s and purchases.customer_email = customer.email and purchase_date BETWEEN DATE_SUB(%s, INTERVAL 1 YEAR) and %s group by customer.email order by count(ticket.ticket_id) DESC limit 10'
    args = (airline_name, date, date)
    
    try:
        cursor.execute(query, args)
    except Exception as e:
        print(e)
        return json.dumps({"success":"false", "message": "database query failed"})
    data = cursor.fetchall()
    for d in data:
        email = d['email']
        query = 'select name, departure_airport, departure_time, arrival_airport, arrival_time from customer natural join purchases natural join ticket natural join flight where customer.email = purchases.customer_email and customer.email = %s and flight.airline_name = %s'
        args = (email, airline_name)
        cursor.execute(query,args)
        f = cursor.fetchall()
        d.update({"flights":f})

    return json.dumps({"success":"true", "message": "database query succeeded, viewfrequentcustomers", "customers":data},indent=4,sort_keys=True, default=str)

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

if __name__ == "__main__":
    app.secret_key = "I gotta s3cret key that youll never know"
    app.run('127.0.0.1', 5000, use_debugger = True)
