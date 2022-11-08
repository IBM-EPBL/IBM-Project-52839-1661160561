from flask import Flask, render_template, request, redirect, url_for, session
import re
import ibm_db
import ibm_db_dbi

conn_string = input("Enter Connection String : ")

try:
    ibm_db_conn = ibm_db.connect(conn_string, " ", " ")
    print("connected")
except Exception as e:
    print(e)

conn = ibm_db_dbi.Connection(ibm_db_conn)

app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('register'))
	
@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'rollnumber' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		rollnumber = request.form['rollnumber']
		cursor = conn.cursor()
		select = f"SELECT * FROM user WHERE (username = \'{username}\') OR (rollnumber = \'{rollnumber}\') OR (email = \'{email}\');"
		print(select)
		cursor.execute(select)
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email or not rollnumber:
			msg = 'Please fill out the form !'
		else:
			insert = f"INSERT INTO user VALUES (\'{rollnumber}\', \'{email}\', \'{username}\', \'{password}\');"
			cursor.execute(insert)
			conn.commit()
			msg = 'You have successfully registered !'
		# return render_template('login.html', msg = msg)
		return redirect(url_for('login'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
		return render_template('register.html', msg = msg)
	return render_template('register.html', msg = msg)
	# return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		select = f"SELECT * FROM user WHERE username = \'{username}\' AND password = \'{password}\';"
		print(select)
		cursor = conn.cursor()
		cursor.execute(select)
		account = cursor.fetchone()
		print(account)
		print(type(account))
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[2]
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.secret_key = '01234'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run()
Foo