#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port=8889,
                       user='root',
                       password='root',
                       db='travel',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/searchingFlights', methods=['GET', 'POST'])
def searchingFlights():
	airlineName = request.form['airline_name']
	departDate = request.form['depart_date']
	flightNum = request.form['flight_number']
	cursor = conn.cursor()
	#make a query
	#SELECT * FROM Flight WHERE airlineName = %s and flightNum = %i and departDate = %d 
	query = 'SELECT * FROM Flight WHERE airline_name = %s and flight_number = %s and depart_date = %s'
	cursor.execute(query, (airlineName,flightNum,departDate))
	#stores the results in a variable
	data = cursor.fetchall()
	print(data)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('index.html',data2=data,airline_n=airlineName,departD=departDate,flightN=flightNum)

#flightRatings
@app.route('/flightRatings', methods=['GET', 'POST'])
def flightRatings():
    cursor = conn.cursor()
	#make a query
	#WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
    email=session['email']
    query = 'SELECT airline_name FROM Staff WHERE username=%s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data2 = cursor.fetchone()
    print(data2)
    cursor.close()
    cursor = conn.cursor()
    query = 'SELECT * FROM Feedback WHERE airline_name=%s'
    cursor.execute(query, (data2['airline_name']))
	#stores the results in a variable
    data2 = cursor.fetchone()
    print(data2)
	#GROUP BY (flight_number,depart_date,depart_time)
    query = 'SELECT avg(ratings) FROM Feedback WHERE airline_name=%s'
    cursor.execute(query, (data2['airline_name']))
	#stores the results in a variable
    data2 = cursor.fetchone()
    print(data2)
    cursor.close()
    return render_template()

#View Booking agents
@app.route('/ViewBookingAgents', methods=['GET', 'POST'])
def ViewBookingAgents():
    cursor = conn.cursor()
	#WHERE   create_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
	#where month(order_date)=month(now())-1;
    query = 'SELECT * FROM Ticket NATURAL JOIN Purchase_by_BA WHERE purchase_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE() '
    cursor.execute(query, (data2))
	#stores the results in a variable
    data2 = cursor.fetchone()
    print(data2)
    cursor.close()
    cursor = conn.cursor()
	#WHERE   create_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
	#where month(order_date)=month(now())-1;
    query = 'SELECT * FROM Ticket NATURAL JOIN Purchase_by_BA WHERE purchase_date BETWEEN CURDATE() - INTERVAL 1 YEAR AND CURDATE() '
    cursor.execute(query, (data2))
	#stores the results in a variable
    data2 = cursor.fetchone()
    print(data2)
    cursor.close()
    return render_template
    	
#/frequentCustomers
@app.route('/frequentCustomers', methods=['GET', 'POST'])
def frequentCustomers():
    	
    return render_template

@app.route('/createNewFlights', methods=['GET','POST'])
def createNewFlights():
    	
	email=session['email']
	cursor = conn.cursor()
	#make a query
	#WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	query = 'SELECT airline_name FROM Staff WHERE username=%s'
	email=session['email']
	cursor.execute(query, (email))
	#stores the results in a variable
	data2 = cursor.fetchone()
	print(data2['airline_name'])
	cursor.close()
	airplaneID=request.form['airplaneID']
	flightNum=request.form['flightNum']
	departTime=request.form['departTime']
	departDate=request.form['departDate']
	arrivalTime=request.form['arrivalTime']
	arrivalDate=request.form['arrivalDate']
	basePrice=request.form['basePrice']
	airportNameArr=request.form['airportNameArr']
	airportNameDep=request.form['airportNameDep']
	statusF=request.form['statusF']
	print(airplaneID,'airplane ID')
	cursor = conn.cursor()
	#make a query
	#WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	query = 'INSERT into Flight (airline_name,airplane_ID,flight_number,depart_time,depart_date,arrival_date,arrival_time,base_price,airport_name_arrival,airport_name_depart,status_F)\
		values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	email=session['email']
	cursor.execute(query, (data2['airline_name'],airplaneID,flightNum,departTime,departDate,arrivalDate,arrivalTime,basePrice,airportNameArr,airportNameDep,statusF))
	#stores the results in a variable
	conn.commit()
	cursor.close()
	return render_template('airline_staff.html')
    
@app.route('/createNewAirplane',methods=['GET','POST'])
def createNewAirplane():
    
	email=session['email']
	cursor=conn.cursor()
	query = 'SELECT airline_name FROM Staff WHERE username=%s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data2 = cursor.fetchone()
	print(data2)
	cursor.close()
	cursor=conn.cursor()
	airplaneID=request.form['airplaneID']
	seats=request.form['seats']
	query = 'INSERT into Flight (airplane_ID,flight_number,airline_name)values (%s,%s,%s)'
	cursor.execute(query, (airplaneID,seats,data2['airline_name']))
	#stores the results in a variable
	conn.commit()
	cursor.close()
	return render_template('airline_staff.html')

@app.route('/createNewAirport',methods=['GET','POST'])
def createNewAirport():
    	
	email=session['email']
	cursor=conn.cursor()
	query = 'SELECT airline_name FROM Staff WHERE username=%s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data2 = cursor.fetchone()
	print(data2)
	cursor.close()
	cursor=conn.cursor()
	city=request.form['city']
	query = 'INSERT into Flight (airplane_ID,flight_number,airline_name)values (%s,%s,%s)'
	cursor.execute(query, (airplaneID,seats,data2['airline_name']))
	#stores the results in a variable
	conn.commit()
	cursor.close()
	return render_template('airline_staff.html')
@app.route('/defaultFlights',methods=['GET','POST'])
def defaultFlights():
    	
	cursor = conn.cursor()
	#make a query
	#WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	query = 'SELECT * FROM Staff Natural Join Flight WHERE username=%s and depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	email=session['email']
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchall()
	print(data)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('airline_staff.html',flights=data)
    
#this one is airline staff
@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
    #if one of them is empty 
	#else they are both empty which means their is no flight
	fromCiorAirport = request.form['fromCiorAirport']
	toCiorAirport = request.form['toCiorAirport']
	departDate = request.form['departDate']
	returnDate = request.form['returnDate']
	email=session['email']
	#need a default arg
	cursor = conn.cursor()
	#make a query
	query = 'SELECT * FROM Staff Natural Join Flight WHERE username=%s and airport_name_arrival = %s and airport_name_depart = %s and depart_date = %s and arrival_date=%s'
	cursor.execute(query, (email,airlineName,flightNum,departDate,returnDate))
	#stores the results in a variable
	data = cursor.fetchall()
	print(data)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('airline_staff.html',data2=data,airline_n=airlineName,departD=departDate,flightN=flightNum)
    
#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	cust = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Booking_Agent WHERE email = %s and passwrd = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	BA = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Staff WHERE username = %s and password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	staff = cursor.fetchone()
	print(staff)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(cust):
		
		session['email']=email
		return redirect(url_for(''))
	elif(BA):
    		
		session['email'] = email
		return redirect(url_for(''))
	elif(staff):
    		
		session['email'] = email
		print(email,'looooooogginnn')
		return redirect(url_for('defaultFlights',email=email))
	else:
    	
		error = 'Invalid login or username'
		return render_template('login.html',error=error)
   	
#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
