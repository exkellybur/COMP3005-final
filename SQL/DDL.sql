DROP TABLE IF EXISTS Members CASCADE;
DROP TABLE IF EXISTS Routines CASCADE;
DROP TABLE IF EXISTS FitnessGoals CASCADE;
DROP TABLE IF EXISTS HealthMetrics CASCADE;
DROP TABLE IF EXISTS Trainers CASCADE;
DROP TABLE IF EXISTS PersonalSessions CASCADE;
DROP TABLE IF EXISTS Availability CASCADE;
DROP TABLE IF EXISTS GroupClasses CASCADE;
DROP TABLE IF EXISTS Room CASCADE;
DROP TABLE IF EXISTS Admins CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS Billing CASCADE;
DROP TABLE IF EXISTS ClassRegistrations CASCADE;


CREATE TABLE IF NOT EXISTS Members (
	memberID SERIAL,
	email VARCHAR(255) NOT NULL,
	pass VARCHAR(255) NOT NULL,
	memberName VARCHAR(255) NOT NULL,
	gender VARCHAR(255),
	PRIMARY KEY(memberID)
);

CREATE TABLE IF NOT EXISTS Routines(
	routineID SERIAL,
	memberID INT,
	description TEXT NOT NULL,
	PRIMARY KEY(routineID),
	FOREIGN KEY(memberID) REFERENCES Members
);

CREATE TABLE IF NOT EXISTS FitnessGoals(
	goalID SERIAL,
	memberID INT,
	goalWeight INT NOT NULL,
	goalDate DATE NOT NULL,
	PRIMARY KEY(goalID),
	FOREIGN KEY(memberID) REFERENCES Members
);

CREATE TABLE IF NOT EXISTS HealthMetrics(
	metricID SERIAL,
	memberID INT,
	height INT NOT NULL,
	weight INT NOT NULL,
	muscleMass INT,
	PRIMARY KEY(metricID),
	FOREIGN KEY(memberID) REFERENCES Members
);

CREATE TABLE IF NOT EXISTS Trainers(
	trainerID SERIAL,
	email VARCHAR(255) NOT NULL,
	pass VARCHAR(255) NOT NULL,
	trainerName VARCHAR(255) NOT NULL,
	PRIMARY KEY(trainerID)
);

CREATE TABLE IF NOT EXISTS Availability(
	availabilityID SERIAL,
	trainerID INT,
	startTime TIME NOT NULL,
	endTime TIME NOT NULL,
	availDate DATE NOT NULL,
	PRIMARY KEY(availabilityID),
	FOREIGN KEY(trainerID) REFERENCES Trainers
);

CREATE TABLE IF NOT EXISTS Rooms(
	roomID SERIAL,
	roomName VARCHAR(255),
	booked BOOL DEFAULT FALSE,
	PRIMARY KEY(roomID)
);

CREATE TABLE IF NOT EXISTS PersonalSessions(
	sessionID SERIAL,
	memberID INT,
	trainerID INT,
	startTime TIME,
	endTime TIME,
	sessionDay DATE,
	PRIMARY KEY(sessionID),
	FOREIGN KEY(memberID) REFERENCES Members,
	FOREIGN KEY(trainerID) REFERENCES Trainers
);

CREATE TABLE IF NOT EXISTS GroupClasses(
	classID SERIAL,
	roomID INT,
	trainerID INT,
	className VARCHAR(255),
	startTime TIME,
	endTime TIME,
	classDay DATE,
	PRIMARY KEY(classID),
	FOREIGN KEY(roomID) REFERENCES Rooms,
	FOREIGN KEY(trainerID) REFERENCES Trainers
);

CREATE TABLE IF NOT EXISTS Billing(
	billingID SERIAL,
	memberID INT,
	amount DECIMAL(10,2),
	payFor VARCHAR(255),
	PRIMARY KEY(billingID),
	FOREIGN KEY(memberID) REFERENCES Members
);

CREATE TABLE IF NOT EXISTS Admins(
	adminID SERIAL,
	email VARCHAR(255),
	pass VARCHAR(255),
	adminName VARCHAR(255),
	PRIMARY KEY(adminID)
);

CREATE TABLE IF NOT EXISTS Equipment(
	equipmentID SERIAL,
	equipName VARCHAR(255),
	lastMaintenance DATE,
	nextMaintenance DATE,
	PRIMARY KEY(equipmentID)
);

CREATE TABLE IF NOT EXISTS ClassRegistrations (
    registrationID SERIAL,
    memberID INT,
    classID INT,
    PRIMARY KEY (registrationID),
    FOREIGN KEY (memberID) REFERENCES Members(memberID),
    FOREIGN KEY (classID) REFERENCES GroupClasses(classID)
);


