from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("select * from Album where access = 'public' ")
	pub_albums = cursor.fetchall()
	private_albums = []
	access_albums = []
	
	if 'username' in session:
		cursor.execute("select * from Album where access='private' and username = '%s'" % session['username'] )
		private_albums = cursor.fetchall()
		
		cursor.execute("select * from Album where albumid in (select albumid from AlbumAccess where username = '%s') and access='private'" % session['username'])
		access_albums = cursor.fetchall()
		
	cursor.close();
	return render_template("index.html", pub_albums = pub_albums, private_albums = private_albums, access_albums = access_albums)

@main.route('/live') 
def live_route():
	return send_file('templates/live.html')
