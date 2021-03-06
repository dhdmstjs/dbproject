--The following is a list of sql queries used in the project. These are shown with the arguments that are fed into the
--the query dynamically, which are named to be self explanatory. "rec" indicates that it was received from the front end. 
--Some of the queries are shown given the explicit values (of the dates, or email addresses, etc) to make the meaning of the query more clear.
-- Of course, in the project itself, these values are variable and not hard coded. Enjoy.


-- Querying Flights --

--Get flights given departure and arrival airports and a date. Note that the schema we are given is a date-time instead of date,
--so we need to use "between."
SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and departure_time between %s and %s
execute(query, (rec['depart'], rec['arrive'], rec['date'], rec['date']+' 23:59:59'))

--Get flights given departure and arrival airports only
SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s

-- /Querying Flights --

-- Login and Registration --

-- Check if someone has already registered with a given email if they're a customer
SELECT * FROM customer WHERE email = %s
-- if they're registering as an airline staff
SELECT * FROM airline_staff WHERE username = %s
-- if they're registering as a booking agent
SELECT * FROM booking_agent WHERE email = %s

-- /Login and Registration --

--------------------------------------------------------------------------------------------------------------------------------
--View my flights
SELECT airline_name, flight_num, purchase_date, departure_airport, departure_time, arrival_airport, status FROM purchases natural join ticket natural join flight WHERE departure_time > '2018-02-10' and customer_email = "colton@nyu";

--Customer spending

--Customer total amount spent range of dates:
SELECT sum(price) FROM `purchases` natural join `ticket` natural join flight 
where customer_email = "colton@nyu" and purchase_date BETWEEN "2017-05-1" and "2019-05-4" 
GROUP BY YEAR(purchase_date), MONTH(purchase_date);

--Booking Agent-----------------
-- Total over period of time
SELECT .10*sum(price) as sump FROM `booking_agent` natural join purchases natural join ticket natural join flight 
where purchase_date BETWEEN %s and %s and booking_agent.booking_agent_id = %s

--Average ticket price commission
SELECT .10*sum(price)/count(ticket_id) as avg_ticket_price FROM `booking_agent` natural join purchases natural join ticket natural join flight where purchase_date BETWEEN %s and %s

--Total Number of Tickets sold
SELECT count(ticket_id) as total_sold FROM `booking_agent` natural join purchases natural join ticket natural join flight where purchase_date BETWEEN %s and %s

--Booking Agent Top 5 customers from Number of tickets sold


--Booking Agent Top 5 customers from commission
-- We use the MYSQL DATE_SUB function often to get a range of dates given one date. 
-- For instance, BETWEEN DATE_SUB(%s INTERVAL 1 YEAR) and %s will give the range of one year given the same date for both %s.
SELECT .10*sum(price) as sump FROM `booking_agent` natural join purchases natural join ticket natural join flight 
where booking_agent.email = %s and purchase_date BETWEEN DATE_SUB(%s INTERVAL 1 YEAR) and %s 
group by customer_email 
ORDER BY `sump` DESC 
limit 5

--Booking Agent Top 5 customers from number of tickets sold
--We do this as part of a separate query so that we can order by a different value and use the limit key word to only return 5
SELECT customer_email, count(ticket_id) as count_t
FROM `booking_agent` natural join purchases natural join ticket natural join flight 
where booking_agent.email = %s and purchase_date BETWEEN DATE_SUB("2018-05-05", INTERVAL 6 MONTH) and "2018-05-05" 
group by customer_email 
ORDER BY count(ticket_id) DESC 
limit 5


--/Booking Agent-----------------

--Airline Staff-------------------------------
--Airline staff get airline:
select airline_name from airline_staff where airline_staff.username = "dirty_dan@gmail.com"

--Airline Staff Get flights:
SELECT * FROM flight where airline_name = "American Airlines"

--Get Customer list from flight number:
SELECT customer_email, name, date_of_birth from flight natural join ticket natural join purchases natural join customer 
where flight_num = "98765" and purchases.customer_email = customer.email


--Get top Booking agents based on commission:
SELECT booking_agent.email, sum(flight.price) * .10 as commission
FROM purchases natural join ticket natural join flight, booking_agent
where purchases.booking_agent_id = booking_agent.booking_agent_id
and flight.airline_name = "China Eastern"
and purchase_date between DATE_SUB("2018-05-05", INTERVAL 1 YEAR) and "2018-05-05"
group by booking_agent.booking_agent_id
order by sum(flight.price) desc
limit 5

--Get top booking agents based on tickets past year
SELECT booking_agent.email, count(ticket_id) as tickets
FROM purchases natural join ticket natural join flight, booking_agent
where purchases.booking_agent_id = booking_agent.booking_agent_id
and flight.airline_name = "China Eastern"
and purchase_date between DATE_SUB("2018-05-05", INTERVAL 1 YEAR) and "2018-05-05"
group by booking_agent.booking_agent_id
order by count(ticket_id) desc
limit 5

--Get top booking agents based on tickets past month
SELECT booking_agent.email, count(ticket_id) as tickets
FROM purchases natural join ticket natural join flight, booking_agent
where purchases.booking_agent_id = booking_agent.booking_agent_id
and flight.airline_name = "China Eastern"
and purchase_date between DATE_SUB("2018-05-05", INTERVAL 1 MONTH) and "2018-05-05"
group by booking_agent.booking_agent_id
order by count(ticket_id) desc
limit 5


--Get Frequent customers for a given airline for the last year
--We rank them by number of tickets purchased and take at most 10 of them
SELECT customer.email, count(ticket.ticket_id) from flight natural join ticket natural join purchases natural join customer 
where airline_name = "China Eastern" and purchases.customer_email = customer.email 
and purchase_date BETWEEN DATE_SUB("2018-05-05", INTERVAL 1 YEAR) and "2018-05-05"
group by customer.email 
order by count(ticket.ticket_id) DESC
limit 10

--Get flights for a customer for  given airline
select * from customer natural join purchases natural join ticket natural join flight 
where customer.email = purchases.customer_email and customer.email = "colton@nyu" and flight.airline_name = "Korean Air"

--View Reports: total amount of tickets sold based on range of dates
SELECT count(ticket.ticket_id) as count_t from flight natural join ticket natural join purchases
where airline_name = "China Eastern"
and purchase_date BETWEEN "2018-01-05" and "2018-10-05"

--Comparison of Revenue earned for the last month and the last year:
--Revenue from direct sales for the last month
select sum(price) as sump from purchases natural join ticket natural join flight 
where airline_name = "China Eastern" and purchases.booking_agent_id IS NULL

--Revenue from Booking agent booked sales:
--Here, revenue takes into consideration the commission that must be paid to the booking agents from the price.
select sum(price)- .10*sum(price) as sump from purchases natural join ticket natural join flight 
where airline_name = "China Eastern" and purchases.booking_agent_id IS NOT NULL

--Most popular destinations for last 3 months:
select airport_city, count(ticket_id) as count_t from airport, flight natural join ticket natural join purchases
where airport.airport_name = flight.arrival_airport
and flight.departure_time BETWEEN DATE_SUB("2018-05-05", INTERVAL 3 MONTH) and "2018-05-05"
group by airport_city

-- Most popular destinations for the last year:
select airport_city, count(ticket_id) as count_t from airport, flight natural join ticket natural join purchases
where airport.airport_name = flight.arrival_airport
and flight.departure_time BETWEEN DATE_SUB("2018-05-05", INTERVAL 1 YEAR) and "2018-05-05"
group by airport_city

--Forms:
--The sql insertion queries are kept very basic. The bulk of the work for table insertions is kept in the server and frontend 
-- to make sure that the correct values are inserted in the right places.
--Create Flight
insert into flight values(%s,%s, %s, %s, %s, %s, %s, %s, %s)

--Update Flight Status
UPDATE `flight` SET `status` = %s WHERE `flight`.`airline_name` = %s AND `flight`.`flight_num` = %s;

--Add Airplane
insert into airplane values(%s, %s, %s);

--Add Airport
insert into `airport` values(%s, %s);

--/Airline Staff-------------------------------

