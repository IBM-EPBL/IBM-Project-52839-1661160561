from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/welcome' , methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
       
    return render_template('out.html',name=user,email=email,phone=phone)

app.run(debug=True , port=8080)