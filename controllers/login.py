from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors
import hashlib, uuid
import time
from userUpdate import *

login = Blueprint('login', __name__, template_folder='templates')



@login.route('/login', methods=['GET'])
def user_login():
	if 'username' in session:
		return redirect(url_for('user.user_edit_info'))
	return render_template("login.html")


@login.route('/api/v1/login', methods=['POST'])
def user_login_api():
	login_user_info = request.get_json()
	username = login_user_info['username']
	password = login_user_info['password']
	
	if not (username and password):
		error_json = json.dumps({"errors": [{"message": "You did not provide the necessary fields"}]})
		error_info = Response(error_json, status = 422, mimetype = "application/json")
		return error_info
	
	if 'username' in session:
		user_info = json.dumps({"username": session['username']});
		return user_info
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM User WHERE username = '%s' " % username)
	usr_pwd = cursor.fetchall()
	if not usr_pwd:
		error_json = json.dumps({"errors": [{"message": "Username does not exist"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		cursor.close()
		return error_info
	
	password_split = usr_pwd[0]['password'].split("$")
	algorithm = password_split[0]
	salt = password_split[1]
	password_correct = password_split[2]
	
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()
	
	if password_correct != password_hash:
		error_json = json.dumps({"errors": [{"message": "Password is incorrect for the specified username"}]})
		error_info = Response(error_json, status = 422, mimetype = "application/json")
		cursor.close()
		return error_info
		
	session['username'] = username
	session['firstname'] = usr_pwd[0]['firstname']
	session['lastname'] = usr_pwd[0]['lastname']
	cursor.close()
	
	user_info = json.dumps({"username": session['username']});
	return user_info


	'''
	options = {
		"error": False
	}
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	message = ""
	if 'username' in session:
		if "url" in request.args:
			url = request.args.get("url")
			return redirect(url)
		return redirect(url_for('main.main_route'))
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		cursor.execute("SELECT * FROM User WHERE username = '%s' " % username)
		usr_pwd = cursor.fetchall()

		message = "Login Successful!"
		if not usr_pwd:
			options = {
				"error": True,
				"id": "error_username"
			}
			message = "Username does not exist"
			cursor.close()
			return render_template("login.html", message = message, **options)
		password_split = usr_pwd[0]['password'].split("$")
		algorithm = password_split[0]
		salt = password_split[1]
		password_correct = password_split[2]

		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()

		if password_correct != password_hash:
			message = "Password is incorrect for the specified username"
			options = {
				"error": True,
				"id": "error_combo"
			}
			cursor.close()
			return render_template("login.html", message = message, **options)

		session['username'] = username
		session['firstname'] = usr_pwd[0]['firstname']
		session['lastname'] = usr_pwd[0]['lastname']
                
		cursor.close()
		if "url" in request.args:
			url = request.args.get("url")
			return redirect(url)
		return redirect(url_for('main.main_route'))
	cursor.close()
	return render_template("login.html", message = message, **options)
	'''
