from os import listdir 
from os.path import isfile, join
import hashlib
import os

username = '' 
mypath = "static/images"
count = {}
count["I love sports"] = -1
count["I love football"] = -1
count["Around The World"] = -1
count["Cool Space Shots"] = -1

for f in listdir(mypath):
	if isfile(join(mypath, f)):
		names = f.split('.')	
		album_name = names[0].split('_')[0]
		id = 0
		title = ''
		if album_name == 'sports':
			username = 'sportslover'
			id = 1
			title = "I love sports"

		elif album_name == 'football':
			username = 'sportslover'
			id = 2
			title = "I love football"
		elif album_name == 'world':
			username = 'traveler'
			id = 3
			title = "Around The World"
		elif album_name == 'space':
			username = 'spacejunkie'
			id = 4
			title = "Cool Space Shots"

		name_type = names[0] + '.' + names[1]
		m = hashlib.md5(username + title + name_type)
		count[title] += 1
		#print("INSERT INTO Photo VALUES ('%s', '%s', '2016-01-01'" % (names[0], names[1]))
		#print("INSERT INTO Contains VALUES (%d, '%s', '%s', %d)" % (id, names[0], "", count[title]))
		os.rename(mypath + '/' + name_type, mypath +'/' + m.hexdigest() + '.' + names[1])
		print("INSERT INTO Photo VALUES ('%s', '%s', \"2016-01-01\");" % (m.hexdigest(), names[1]))
		print("INSERT INTO Contain VALUES (%d, '%s', '%s', %d);" % (id, m.hexdigest(), "", count[title]))
