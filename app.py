from flask import *
import mysql.connector
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
from random import *
import os
from dotenv import load_dotenv

current_directory = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path)

# initialize first flask
app = Flask(__name__)
mail = Mail(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp=randint(000000,999999)

print(os.environ.get('MAIL_USERNAME'))
print(os.environ.get('MAIL_PASSWORD'))



def db_connection():
  connection = mysql.connector.connect(
  host="mysql-1ed7bbbc-wlmycn-2bde.aivencloud.com",
  user="nethra",
  password="AVNS_VZBjSvRHMNrTujGWv84",
  port="26098",
  database="defaultdb")
  return connection

@app.route('/', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html',message="")
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		query = f"SELECT * from login_flask_345 where username = '{username}' and password = '{password}'"
		connection = db_connection()
		connection_cursor = connection.cursor()
		connection_cursor.execute(query)
		result = connection_cursor.fetchall()
		print(result)
		if len(result)>0:
			message="login success"
		elif result == []:
			message="user not found"
		return render_template('login.html',message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
		message=" "
		if request.method == 'GET':
			return render_template('register.html', message="please fill out the form")
		elif request.method == 'POST':
			phonenum=request.form['phonenum']
			password = request.form['password']
			email = request.form['email']
			username = request.form['username']
			if 'email' in request.form:
				query= f"SELECT * from login_flask_345 where email = '{email}'"
				connection = db_connection()
				connection_cursor = connection.cursor()
				connection_cursor.execute(query)
				users=connection_cursor.fetchall()
				print(len(users))
				if len(users)>0:
					message = "The email address already exists"
					connection_cursor.close()
					connection.close()
					return render_template('register.html', message=message)
				else:
					query= f"INSERT INTO login_flask_345 (username,email,password,phonenum) VALUES ('{username}','{email}', '{password}','{phonenum}');"
					connection_cursor.execute(query)
					connection.commit()
					connection_cursor.close()
					connection.close()
					message='Registration successful.....'
					username=os.environ.get('MAIL_USERNAME')
					print(username)
					msg = Message(subject='OTP',sender=username,recipients = [email] )
					msg.body = str(otp)
					mail.send(msg)
					return render_template('verify.html')
			else:
				message = "Please enter an email address"
			return render_template('register.html')

@app.route('/validate', methods=['POST'])
def validate():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return redirect(url_for('register.html'))

if __name__=="__main__":
	app.run(debug= True)









