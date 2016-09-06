from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors
import hashlib
import time
import os

album = Blueprint('album', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	options = {
		"edit": True
	}
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	albumid = request.args.get('id')
	if not albumid:
		abort(404)
	if not albumid.isdigit():
		abort(404)
		
	if "username" not in session:
		cursor.close()
		return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/album/edit?id='+albumid, code=401)
	
	cursor.execute("SELECT username, title, access FROM Album WHERE albumid = %s" % (albumid))
	album_info = cursor.fetchall()
	
	if not album_info:
		abort(404)

	if session['username'] != album_info[0]['username']:
		cursor.close()
		print("11111")
		abort(403)

	try:
		if request.method == 'POST':
			if "username" in session and album_info[0]['username']==session['username']: 
				if request.form.get('op') == 'revoke':
					cur_user = request.form.get('username')
					cursor.execute("DELETE FROM AlbumAccess WHERE albumid = %s and username = '%s' " % (albumid, cur_user))
					cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))
				elif request.form.get('op') == 'grant':
					cur_user = request.form.get('username')
					cursor.execute("SELECT * FROM User WHERE username = '%s'" % cur_user)
					usr = cursor.fetchall()
					
					cursor.execute("SELECT * FROM AlbumAccess WHERE username = '%s' and albumid = %s" % (cur_user,albumid) )
					access_info = cursor.fetchall()
					
					if usr and cur_user != session['username'] and not access_info:
						cursor.execute("INSERT INTO AlbumAccess VALUES (%s, '%s')" % (albumid, cur_user))
						cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))
				elif request.form.get('op') == 'access':
					access_type = request.form.get('access')
					if access_type == 'public' and album_info[0]['access']=='private':
						cursor.execute("DELETE FROM AlbumAccess WHERE albumid = %s " % (albumid))
					if access_type != album_info[0]['access']:
						cursor.execute("UPDATE Album SET access = '%s' WHERE albumid = %s " % (access_type, albumid))
						cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))
					                    
                    
				# if add:
				elif 'add' in request.form.values():
					#file = request.files['uploaded_file']
					file = request.files['file']
					if file.filename != '':
						username = album_info[0]['username']
						title = album_info[0]['title']
						name_fmt = file.filename.split('.')
						name = name_fmt[0]
						fmt = name_fmt[1]
						uploaded_picid = hashlib.md5(username + title + file.filename).hexdigest()
						file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_picid + '.' + fmt))
						cursor.execute("INSERT INTO Photo VALUES ('%s', '%s', '%s')" % (uploaded_picid, fmt, time.strftime("%Y-%m-%d")))
						cursor.execute(("SELECT max(sequencenum) FROM Contain WHERE albumid = %s") % albumid)
						result = cursor.fetchall()
						max_seqnum = result[0]['max(sequencenum)']
						if max_seqnum == None:
							max_seqnum = -1
						cursor.execute("INSERT INTO Contain VALUES (%s, '%s', '', %d)" % (albumid, uploaded_picid, int(max_seqnum)+1))
						cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))


				elif 'delete' in request.form.values():
					picid = request.form.get('picid')
					cursor.execute("SELECT * FROM Photo WHERE picid = '%s'" % (picid))
					checkid = cursor.fetchall()
					if not checkid:
						cursor.close()
						abort(404)
					#update album's lastupdatedtime
					cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))
					#delete record from Contain
					cursor.execute("DELETE FROM Contain WHERE picid = '%s' " % picid)
					#delete file and delete from Photo
					cursor.execute("SELECT format FROM Photo WHERE picid = '%s' " % picid)
					format_list = cursor.fetchall()

					format = format_list[0]['format']
					photo_name = picid + '.' + format
					cursor.execute("DELETE FROM Photo WHERE picid = '%s' " % picid)
					os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_name))

				mysql.connection.commit()

		cursor.execute("SELECT p.picid, p.format, c.sequencenum FROM Contain c, Photo p WHERE c.albumid = %s AND p.picid = c.picid ORDER BY sequencenum" % albumid)
		pic_list = cursor.fetchall()

	except:
		cursor.close()
		abort(404)


        # for refreshing
	cursor.execute("SELECT username, title, access FROM Album WHERE albumid = %s" % (albumid))
	album_info = cursor.fetchall()

        access_table = {}
        access_table['show'] = True if "username" in session and album_info[0]['access']=='private' and album_info[0]['username']==session['username'] else False
        access_table['other_users'] = []
        cursor.execute("SELECT username FROM AlbumAccess WHERE albumid = %s" % (albumid))
        for user_item in cursor.fetchall():
            access_table['other_users'].append( user_item['username'] )


	cursor.close()
        return render_template("album.html", pic_list = pic_list, album_info = album_info[0], access_table = access_table, albumid=albumid,**options)


	
	
	
###################################################
@album.route('/album', methods=['GET'])
def album_route():
	options = {
		"edit": False,
		"owner": False
	}
	albumid = request.args.get('id')
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT username, title, access FROM Album WHERE albumid = %s" % (albumid))
	checkid = cursor.fetchall()
	if checkid[0]['access'] == 'private':
		if 'username' not in session:
			return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/album?id=' + albumid, code=401)
	if 'username' in session and session['username'] == checkid[0]['username']:
		options["owner"] = True
			
	
	'''
	albumid = request.args.get('id')
	if not albumid:
		abort(404)
	if not albumid.isdigit():
		abort(404)
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT username, title, access FROM Album WHERE albumid = %s" % (albumid))
	checkid = cursor.fetchall()
	if not checkid:
		abort(404)
	if checkid[0]['access'] == 'private':
		if 'username' not in session:
			return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/album?id=' + albumid)
		if session['username'] == checkid[0]['username']:
			pass
		else:
			cursor.execute(("SELECT username FROM AlbumAccess WHERE albumid = %s and username = '%s'") % (albumid, session['username']))
			if not cursor.fetchall():
				abort(403)

        if 'username' in session:
	        if session['username'] == checkid[0]['username']:
		        options["owner"] = True
		
	
	
	cursor.execute("SELECT p.picid, p.format, c.sequencenum FROM Contain c, Photo p WHERE c.albumid = %s AND p.picid = c.picid ORDER BY sequencenum" % albumid)
	pic_list = cursor.fetchall()

	cursor.close()
	return render_template("album.html", pic_list = pic_list, album_info = checkid[0],  albumid=albumid,**options)
	'''
	return render_template("album.html", albumid=albumid, **options)








###################################################
@album.route('/api/v1/album/<int:albumid>', methods=['GET'])
def album_api_get(albumid):
	if not albumid:
		abort(404)
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT username, title, access FROM Album WHERE albumid = %s" % (albumid))
	album_info = cursor.fetchall()
	
	if not album_info:
		error_json = json.dumps({"errors": [{"message": "The requested resource could not be found"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		return error_info
	
	if album_info[0]['access'] == 'private':
		if 'username' not in session:
			error_json = json.dumps({"errors": [{"message": "You do not have the necessary credentials for the resource"}]})
			error_info = Response(error_json, status = 401, mimetype = "application/json")
			return error_info
		
		if session['username'] != album_info[0]['username']:
			error_json = json.dumps({"errors": [{"message": "You do not have the necessary permissions for the resource"}]})
			error_info = Response(error_json, status = 403, mimetype = "application/json")
			return error_info
	
        
	#TODO: get all album info and return
	cursor.execute("SELECT * FROM Album WHERE albumid = %s" % (albumid))
	album_info = cursor.fetchall()[0]
	album_info['created'] = str(album_info['created'])
	album_info['lastupdated'] = str(album_info['lastupdated'])
	
	
	cursor.execute("SELECT c.albumid, c.caption, p.date, p.format, c.picid, c.sequencenum from Contain c, Photo p where c.picid = p.picid and c.albumid = %s ORDER BY sequencenum" % albumid)
	album_info['pics']  = list(cursor.fetchall())
	
	for item in album_info['pics']:
		item['date'] = str(item['date'])
 	
	jsonObj = json.dumps(album_info)
	return jsonObj
	
