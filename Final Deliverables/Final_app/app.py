# create a flask app
from flask import Flask, render_template, request, redirect, url_for
import ibm_db
import re

app = Flask(__name__)

conn = ibm_db.pconnect("DATABASE=BLUDB;"
                       "HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;"
                       "PORT=32733;"
                       "UID=dnp80914;PWD=5OtVWHTwkHw2GmU3;"
                       "PROTOCOL=TCPIP;"
                       "Security=SSL;"
                       "sslConnection=true;"
                       "SSLServerCertificate=DigiCertGlobalRootCA.crt;"
                       "", "", "")

print("Connected to database", conn)


# create a route for the home page
@app.route('/', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        # get the data from the form
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # if nothing is entered in the form
        if not name or not email or not password or not confirm_password:
            message = 'Please fill all the fields!'
            return render_template('register.html', message=message)
        # if the password and confirm password do not match
        elif password != confirm_password:
            message = 'Passwords do not match!'
            return render_template('register.html', message=message)

        #  password length must be 8 or above
        if len(password) < 8:
            message = 'Password must be 8 or more characters'
            return render_template('register.html', message=message)
        # check if the email is valid
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # insert the data into the database
            # check if the username and email already exists in the database
            sql = "SELECT * FROM users WHERE username = '" + name + "' OR email = '" + email + "'"
            stmt = ibm_db.exec_immediate(conn, sql)
            # print("stmt", stmt)
            result = ibm_db.fetch_assoc(stmt)
            # print("result", result)
            if result:
                message = 'The username or email already exists!'
            else:
                sql = "INSERT INTO users (username, email, password) VALUES ('" + name + "', '" + email + "', '" + password + "')"
                ibm_db.exec_immediate(conn, sql)
                message = 'You have successfully registered!'
        else:
            message = 'The email is invalid!'
    return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        # get the data from the form
        name = request.form['username']
        password = request.form['password']
        # if nothing is entered in the form
        if not name or not password:
            message = 'Please fill all the fields!'
            return render_template('login.html', message=message)
        # check if the username and password are valid
        sql = "SELECT * FROM users WHERE username = '" + name + "' AND password = '" + password + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        # print("result", result)
        if result:
            message = 'You have successfully logged in!'
            return render_template('login.html', message=message)
        else:
            message = 'The email or password is incorrect!'
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
