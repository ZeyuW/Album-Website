from flask import *
from extensions import mysql
from flask.ext.mysqldb import MySQLdb
import MySQLdb.cursors, time

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET', 'POST'])
def pic_route():
	options = {
		"owner": False
	}
	picid = request.args.get('id')
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM Photo WHERE picid = '%s'" % (picid))
	checkid = cursor.fetchall()
	if not checkid:
		error_json = json.dumps({"errors": [{"message": "The requested resource could not be found"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		return error_info
	

	"""
        # wu?? what if one pic doesn't belong to any album ? 
	cursor.execute(("SELECT c.albumid, c.caption, c.sequencenum, p.format FROM Contain c, Photo p WHERE c.picid = p.picid AND c.picid = '%s'") % picid)
	pic_list = cursor.fetchall()

	caption = pic_list[0]['caption']
	albumid = pic_list[0]['albumid']
	sequencenum = pic_list[0]['sequencenum']
	fmt = pic_list[0]['format']

	cursor.execute(("SELECT * FROM Album WHERE albumid = %s") % albumid)
	album_info = cursor.fetchall()
	if album_info[0]['access'] == 'private':
		if 'username' not in session:
			return redirect('/5lj4zg/pa2/login?url=/5lj4zg/pa2/pic?id=' + picid)

		if session['username'] == album_info[0]['username']:
			options['owner'] = True
		else:
			cursor.execute(("SELECT username FROM AlbumAccess WHERE albumid = %s and username = '%s'") % (albumid, session['username']))
			if not cursor.fetchall():
				abort(403)
	else:
		if 'username' in session:
			if session['username'] == album_info[0]['username']:
				options['owner'] = True

	if request.method == 'POST':
		if request.form.get('op')=='caption':
			if "username" in session and session['username']==album_info[0]['username']:
				new_caption = request.form.get('caption')
				cursor.execute("UPDATE Contain SET caption = '%s' WHERE albumid = %s and picid = '%s'" % (new_caption, albumid, picid))
				cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), albumid))
				cursor.execute(("SELECT c.caption FROM Contain c, Photo p WHERE c.picid = p.picid AND c.picid = '%s'") % picid)
				caption_list = cursor.fetchall()
				caption = caption_list[0]['caption']
                                 


	'''
	next, previous
	'''
	cursor.execute(("SELECT max(sequencenum) FROM Contain WHERE albumid = %s") % albumid)
	max_seqnum = cursor.fetchall()[0]['max(sequencenum)']

	prev_picid = -1
	if sequencenum != 0:
		cursor.execute(("SELECT picid FROM Contain WHERE albumid = %s AND sequencenum = (%s - 1)") % (albumid, sequencenum))
		result = cursor.fetchall()
		if result:
			prev_picid = result[0]['picid']

	next_picid = -1
	if sequencenum != max_seqnum:
		cursor.execute(("SELECT picid FROM Contain WHERE albumid = %s AND sequencenum = (%s + 1)") % (albumid, sequencenum))
		result = cursor.fetchall()
		if result:
			next_picid = result[0]['picid']	

	cursor.close()
	mysql.connection.commit()


	adjacent = {
		"albumid" : albumid,
		"next_picid" : next_picid,
		"prev_picid" : prev_picid
	}

	"""
	return render_template("pic.html", **options)

@pic.route('/api/v1/pic/<string:picid>', methods=['GET'])
def pic_api_get(picid):
	options = {
		"owner": False
	}
	if not picid:
		error_json = json.dumps({"errors": [{"message": "The requested resource could not be found"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		return error_info
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM Photo WHERE picid = '%s'" % (picid))
	checkid = cursor.fetchall()
	if not checkid:
		error_json = json.dumps({"errors": [{"message": "The requested resource could not be found"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		return error_info
	
        # wu?? what if one pic doesn't belong to any album ? 
	cursor.execute(("SELECT c.albumid, c.caption, c.sequencenum, p.format FROM Contain c, Photo p WHERE c.picid = p.picid AND c.picid = '%s'") % picid)
	pic_list = cursor.fetchall()

	caption = pic_list[0]['caption']
	albumid = pic_list[0]['albumid']
	sequencenum = pic_list[0]['sequencenum']
	fmt = pic_list[0]['format']

	cursor.execute(("SELECT * FROM Album WHERE albumid = %s") % albumid)
	album_info = cursor.fetchall()
	if album_info[0]['access'] == 'private':
		if 'username' not in session:
			return redirect('/b5340568bdcd46b4b5be/pa3/login?url=/b5340568bdcd46b4b5be/pa3/pic?id=' + picid,code=401)

		if session['username'] == album_info[0]['username']:
			options['owner'] = True
		else:
			cursor.execute(("SELECT username FROM AlbumAccess WHERE albumid = %s and username = '%s'") % (albumid, session['username']))
			if not cursor.fetchall():
				error_json = json.dumps({"errors": [{"message": "You do not have the necessary permissions for the resource"}]})
				error_info = Response(error_json, status = 403, mimetype = "application/json")
				return error_info

	else:
		if 'username' in session:
			if session['username'] == album_info[0]['username']:
				options['owner'] = True	

	cursor.execute(("SELECT max(sequencenum) FROM Contain WHERE albumid = %s") % albumid)
	max_seqnum = cursor.fetchall()[0]['max(sequencenum)']

	prev_picid = -1
	if sequencenum != 0:
		cursor.execute(("SELECT picid FROM Contain WHERE albumid = %s AND sequencenum = (%s - 1)") % (albumid, sequencenum))
		result = cursor.fetchall()
		if result:
			prev_picid = result[0]['picid']

	next_picid = -1
	if sequencenum != max_seqnum:
		cursor.execute(("SELECT picid FROM Contain WHERE albumid = %s AND sequencenum = (%s + 1)") % (albumid, sequencenum))
		result = cursor.fetchall()
		if result:
			next_picid = result[0]['picid']	

	cursor.close()
	mysql.connection.commit()


	adjacent = {
		"albumid" : albumid,
		"next_picid" : next_picid,
		"prev_picid" : prev_picid
	}

	json_dic = {}
	json_dic['albumid'] = albumid
	json_dic['caption'] = caption 
	json_dic['format'] = fmt 
	json_dic['next'] = next_picid 
	json_dic['picid'] = picid 
	json_dic['prev'] = prev_picid 

	jsonObj = json.dumps(json_dic)
	return jsonObj

@pic.route('/api/v1/pic/<string:picid>', methods=['PUT'])
def pic_api_post(picid):
	options = {
		"owner": False
	}
	new_picinfo = request.get_json()
	albumid = new_picinfo['albumid']	

	if not picid:
		error_json = json.dumps({"errors": [{"message": "The requested resource could not be found"}]})
		error_info = Response(error_json, status = 404, mimetype = "application/json")
		return error_info

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(("SELECT * FROM Album WHERE albumid = %s") % albumid)
	album_info = cursor.fetchall()
	
	if "username" in session and session['username']==album_info[0]['username']:
		try:
			
			cursor.execute("UPDATE Contain SET caption = '%s' WHERE albumid = %s and picid = '%s'" % (new_picinfo['caption'], new_picinfo['albumid'], new_picinfo['picid']))
			cursor.execute("UPDATE Album SET lastupdated = '%s' WHERE albumid = %s" % (time.strftime("%Y-%m-%d"), new_picinfo['albumid']))
			cursor.execute(("SELECT c.caption FROM Contain c, Photo p WHERE c.picid = p.picid AND c.picid = '%s'") % new_picinfo['picid'])
			caption_list = cursor.fetchall()
			caption = caption_list[0]['caption']
			mysql.connection.commit()
		except:
			error_json = json.dumps({"errors": [{"message": "You did not provide the necessary fields"}]})
			error_info = Response(error_json, status = 422, mimetype = "application/json")
			return error_info
	else:
		error_json = json.dumps({"errors": [{"message": "You do not have the necessary permissions for the resource"}]})
		error_info = Response(error_json, status = 403, mimetype = "application/json")
		return error_info

	json_dic = {}
	json_dic['albumid'] = new_picinfo['albumid']
	json_dic['caption'] = caption 
	json_dic['format'] = new_picinfo['format'] 
	json_dic['next'] = new_picinfo['next'] 
	json_dic['picid'] = new_picinfo['picid'] 
	json_dic['prev'] = new_picinfo['prev'] 
	new_picinfo_json = json.dumps(json_dic)
	return new_picinfo_json






