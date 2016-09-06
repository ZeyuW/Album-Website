from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors
import hashlib
import time

usr_logout = Blueprint('usr_logout', __name__, template_folder='templates')

@usr_logout.route('/logout', methods=['GET'])
def logout():
	return render_template("logout.html")	

@usr_logout.route('/api/v1/logout', methods=['POST'])
def logout_cur_user():
	if 'username' not in session:
		error_json = json.dumps({"errors": [{"message": "You do not have the necessary credentials for the resource"}]})
		error_info = Response(error_json, status = 401, mimetype = "application/json")
		return error_info

	session.pop('username', None)
	session.pop('firstname', None)
	session.pop('lastname', None)
	
	logout_info = Response("", status = 204, mimetype = "application/json")
	return logout_info