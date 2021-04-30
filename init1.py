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
    	
    return render_template

#View Booking agents
@app.route('/ViewBookingAgents', methods=['GET', 'POST'])
def ViewBookingAgents():
    	
    return render_template
    	
#/frequentCustomers
@app.route('/frequentCustomers', methods=['GET', 'POST'])
def frequentCustomers():
    	
    return render_template
    
@app.route('/defaultFlights',methods=['GET','POST'])
def defaultsFlights():
    	
	cursor = conn.cursor()
	#make a query
	query = 'SELECT * FROM Staff Natural Join Flight WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	cursor.execute(query, ())
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
	#need a default arg
	'''
	cursor = conn.cursor()
	#make a query
	query = 'SELECT * FROM Staff Natural Join Flight WHERE depart_date < CURDATE() + INTERVAL 30 DAY and CURDATE() < depart_date'
	cursor.execute(query, ())
	#stores the results in a variable
	data = cursor.fetchall()
	print(data)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	'''
	cursor = conn.cursor()
	#make a query
	query = 'SELECT * FROM Staff Natural Join Flight WHERE airline_name = %s and flight_number = %s and depart_date = %s'
	cursor.execute(query, (airlineName,flightNum,departDate))
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
		return redirect(url_for('defaultFlights'))
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
