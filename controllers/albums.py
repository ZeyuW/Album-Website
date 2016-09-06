from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors
import time
import os

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	options = {
		"edit": True
	}
	if "username" not in session:
		return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/albums/edit',code=401)
	
	username = session["username"]
	
	try:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		if request.method == 'POST':
			# if add:
                        print 'request.form.values()', request.form.values()
                        print 'request.form.op', request.form.get('op')
			if 'add' in request.form.values():
				new_album_title = request.form.get('title')
				cursor.execute("INSERT INTO Album (title, created, lastupdated, username) VALUES ('%s', '%s', '%s', '%s') " % (new_album_title, time.strftime("%Y-%m-%d"), time.strftime("%Y-%m-%d"), username))
			elif 'delete' in request.form.values():
				albumid = request.form.get('albumid')

				cursor.execute("select picid from Contain c where c.albumid = %s" % albumid)
				picid_list = cursor.fetchall()
				for picid in picid_list:
					cursor.execute("SELECT format FROM Photo WHERE picid = '%s' " % picid['picid'])
					format_list = cursor.fetchall()
					format = format_list[0]['format']
					photo_name = picid['picid'] + '.' + format
					#print('delete file: %s' % photo_name)
					os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_name))
					cursor.execute("DELETE FROM Photo WHERE picid = '%s' " % picid['picid'])

				cursor.execute("DELETE FROM Contain WHERE albumid = %s " % albumid)

				cursor.execute("DELETE FROM AlbumAccess WHERE albumid = %s " % albumid)
				cursor.execute("DELETE FROM Album WHERE albumid = %s " % albumid)

		mysql.connection.commit()
		cursor.execute("SELECT albumid, title, access  FROM Album WHERE username = '%s'" % username)
		album_list = cursor.fetchall()
		cursor.close()
	except:
		abort(404)
	#if not album_list:
	#	abort(404)
	return render_template("albums.html", username = username, album_list = album_list, **options)


@albums.route('/albums', methods=['GET', 'POST'])
def albums_route():
	options = {
		"edit": False,
		"public":False
	}
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	if "username" in request.args:
		username = request.args.get('username')
		cursor.execute("SELECT * FROM User WHERE username = '%s'" % username)
		user = cursor.fetchall()
		if not user:
			abort(404)
		options = {
			"edit": False,
			"public":True
		}
		cursor.execute("SELECT * FROM Album WHERE username = '%s' and access='public'" % username)
		album_list = cursor.fetchall()
		cursor.close()
		return render_template("albums.html", username = username, album_list = album_list, **options)
	elif 'username' in session:
		cursor.execute("SELECT * FROM Album WHERE username = '%s'" % session['username'])
		album_list = cursor.fetchall()
		cursor.close()
		return render_template("albums.html", album_list = album_list, **options)
	cursor.close()
	return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/albums',code=401)		
	'''
	try:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute("SELECT albumid, title  FROM Album WHERE username = '%s'" % username)
				album_list = cursor.fetchall()

				cursor.close()
			except:
				abort(404)
			if not album_list:
				abort(404)


	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	if "username" in request.args:
		username = request.args.get('username')
		cursor.execute("SELECT * FROM User WHERE username = '%s'" % username)
		user = cursor.fetchall()
		if not user:
			abort(404)
		cursor.execute("SELECT * FROM Album WHERE username = '%s' and access='public'" % username)
		album_list = cursor.fetchall()
		cursor.close()
		return render_template("albums.html", username = username, album_list = album_list, **options)
	'''
	return render_template("albums.html", username = session['username'], album_list = album_list, **options)

