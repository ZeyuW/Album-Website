DROP TABLE if exists Contain;
DROP TABLE if exists User;
DROP TABLE if exists Album;
DROP TABLE if exists AlbumAccess;
DROP TABLE if exists Photo;


CREATE TABLE User (
	username varchar(20) NOT NULL PRIMARY KEY,
	firstname varchar(20) NOT NULL,
	lastname varchar(20) NOT NULL,
	password varchar(256) NOT NULL,
	email varchar(40) NOT NULL
);

CREATE TABLE Album (
	albumid int NOT NULL AUTO_INCREMENT,
	title varchar(50) NOT NULL,
	created DATE NOT NULL,
	lastupdated DATE NOT NULL,
	username varchar(20) NOT NULL REFERENCES User(username),
	access ENUM('public', 'private') DEFAULT 'private' NOT NULL,
	PRIMARY KEY(albumid)
);

CREATE TABLE AlbumAccess (
	albumid int NOT NULL REFERENCES Album(albumid),
	username varchar(20) NOT NULL REFERENCES User(username),
	PRIMARY KEY (albumid, username)
);

CREATE TABLE Contain(
	albumid int NOT NULL REFERENCES Album(albumid),
	picid varchar(40) NOT NULL REFERENCES Photo(picid),
	caption varchar(255) NOT NULL,
	sequencenum int NOT NULL,
	PRIMARY KEY (albumid, picid)
);

CREATE TABLE Photo(
	picid varchar(40) NOT NULL PRIMARY KEY,
	format char(3),
	date DATE
);

