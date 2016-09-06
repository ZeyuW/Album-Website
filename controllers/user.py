from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors
import hashlib, time
import uuid
from userUpdate import *

user = Blueprint('user', __name__, template_folder='templates')


check_list = ['username', 'firstname', 'lastname', 'email', 'password1', 'password2']
check_dict = {}
for check_item in check_list:
	check_dict[check_item] = eval( 'check_' + check_item )


@user.route('/user/edit', methods=['GET'])
def user_edit_info():
	if 'username' not in session:
		return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/user/edit', code=401)
	options = {"edit":True}
	return render_template("user.html", **options)


@user.route('/user', methods=['GET'])
def user_info():
	options = {"edit":False}
	if 'username' in session:
		return redirect(url_for('user.user_edit_info'))
	return render_template("user.html", **options)



@user.route('/api/v1/user', methods=['POST'])
def create_new_user():
	new_user_info = request.get_json()

	#check_list = ['username', 'firstname', 'lastname', 'email', 'password1', 'password2']
	rec_list = [ new_user_info[item] for item in check_list ] 
	if None in rec_list:
			error_json = json.dumps({"errors": [{"message": "You did not provide the necessary fields"}]})
			error_info = Response(error_json, status = 422, mimetype = "application/json")
			return error_info

	username, firstname, lastname, email, password1, password2 = rec_list


	options = {"edit":False}
	options['errors'] = []

	if 'username' in session:
		return redirect(url_for('user.user_edit_info'))

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

	for check_item in check_list:
		if check_item=='username':
			cursor.execute("SELECT username FROM User WHERE username = '%s' " % username)
			for err in check_dict[check_item]( eval(check_item),  cursor.fetchall() ):
				options["errors"].append( {'message': err} )
		elif check_item == 'password2': 
			for err in check_dict[check_item]( eval(check_item), password1 ):
				options["errors"].append( {'message': err} ) 
		else:
			for err in check_dict[check_item]( eval(check_item) ):
				options["errors"].append( {'message': err} ) 

	if options["errors"]: 
		user_info_json = json.dumps( options )
		user_info = Response(user_info_json, status = 422, mimetype = "application/json")
		return user_info


	password = password_hash(password1)

	cursor.execute("INSERT INTO User (username, firstname, lastname, password, email) VALUES ('%s', '%s', '%s', '%s', '%s')" % (username, firstname, lastname, password, email))
	mysql.connection.commit()
	cursor.close()

	user_info_json = json.dumps({"username": username, "firstname": firstname, "lastname": lastname, "email": email})
	user_info = Response(user_info_json, status = 201, mimetype = "application/json")
	return user_info



@user.route('/api/v1/user', methods=['GET'])
def get_new_user():
	if 'username' not in session:
		error_json = json.dumps({"errors": [{"message": "You do not have the necessary credentials for the resource"}]})
		error_info = Response(error_json, status = 401, mimetype = "application/json")
		return error_info
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select * from User where username='%s'" % session["username"])
	user_all_info  = cursor.fetchall()
	
	user_info = json.dumps({"username": user_all_info[0]['username'], "firstname": user_all_info[0]['firstname'], "lastname": user_all_info[0]['lastname'], "email": user_all_info[0]['email']})
	return user_info



@user.route('/api/v1/user', methods=['PUT'])
def edit_current_user():
	new_user_info = request.get_json()

	#check_list = ['username', 'firstname', 'lastname', 'email', 'password1', 'password2']
	rec_list = [ new_user_info[item] for item in check_list ] 
	if None in rec_list:
			error_json = json.dumps({"errors": [{"message": "You did not provide the necessary fields"}]})
			error_info = Response(error_json, status = 422, mimetype = "application/json")
			return error_info
	username, firstname, lastname, email, password1, password2 = rec_list

	if 'username' not in session:
		error_json = json.dumps({"errors": [{"message": "You do not have the necessary credentials for the resource"}]})
		error_info = Response(error_json, status = 401, mimetype = "application/json")
		return error_info
	
	if username != session['username']:
		error_json = json.dumps({"errors": [{"message": "You do not have the necessary permissions for the resource"}]})
		error_info = Response(error_json, status = 403, mimetype = "application/json")
		return error_info

	options = {"edit":False}
	options['errors'] = []

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	
	for check_item in check_list:
		if check_item=='username':
			pass
		elif check_item == 'password1':
			if password1 and password2:
				for err in check_dict[check_item]( eval(check_item) ):
					options["errors"].append( {'message': err} )
		elif check_item == 'password2': 
			if password1 and password2:
				for err in check_dict[check_item]( eval(check_item), password1 ):
					options["errors"].append( {'message': err} ) 
		else:
			for err in check_dict[check_item]( eval(check_item) ):
				options["errors"].append( {'message': err} ) 
				
			
	if options["errors"]: 
		user_info_json = json.dumps( options )
		user_info = Response(user_info_json, status = 422, mimetype = "application/json")
		return user_info

	
	session['firstname'] = firstname
	session['lastname'] = lastname
	if password1 and password2:
		password = password_hash(password1)
		cursor.execute("UPDATE User SET password = '%s' where username='%s'" % (password, session["username"]))
	cursor.execute("UPDATE User SET firstname = '%s', lastname = '%s', email = '%s' WHERE username = '%s'" % (firstname, lastname, email, session["username"]))
	mysql.connection.commit()
	cursor.close()

	user_info_json = json.dumps({"username": username, "firstname": firstname, "lastname": lastname, "email": email})
	user_info = Response(user_info_json, status = 201, mimetype = "application/json")
	return user_info