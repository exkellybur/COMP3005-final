--INSERT SAMPLE DATA INTO TABLES 

--Members table
INSERT INTO Members(email, pass, memberName, gender) VALUES
('bill@gmail.com', 'password', 'Bill Duck', 'M'),
('judy@gmail.com', 'abc', 'Judy Cub', 'F');

--Routines table
INSERT INTO Routines (memberID, description) VALUES
(1, 'Heavy lifting 3x a week and 8k steps everyday'),
(2, 'Morning jog followed by sit ups');

--FitnessGoals table 
INSERT INTO FitnessGoals (memberID, goalWeight, goalDate) VALUES
(1, 185, '2024-06-13'),
(2, 130, '2024-04-30');

--HealthMetrics Table
INSERT INTO HealthMetrics (memberID, height, weight, muscleMass) VALUES
(1, 178, 175, 70),
(2, 160, 140, 50);

--Trainers Table 
INSERT INTO Trainers (email, pass, trainerName) VALUES
('trainer1@example.com', 'trainer1', 'Mike Ike'),
('trainer2@example.com', 'trainer2', 'Charlie Brown');

--Availability table
INSERT INTO Availability (trainerID, startTime, endTime, availDate) VALUES
(1, '08:00:00', '10:00:00', '2024-04-24'),
(1, '08:00:00', '10:00:00', '2024-04-22'),
(2, '15:00:00', '17:00:00', '2024-04-23'),
(2, '15:00:00', '17:00:00', '2024-04-27');

--Rooms table
INSERT INTO Rooms (roomName, booked) VALUES
('Cardio Room', FALSE),
('Yoga Room', TRUE),
('Cycling Room', FALSE);

--PersonalSessions table
INSERT INTO PersonalSessions (memberID, trainerID, startTime, endTime, sessionDay) VALUES
(1, 1, '09:00:00', '10:00:00', '2024-04-24'),
(2, 2, '16:00:00', '17:00:00', '2024-04-23');

--GroupClasses table
INSERT INTO GroupClasses (roomID, trainerID, className, startTime, endTime, classDay) VALUES
(2, 1, 'Morning Yoga', '08:00:00', '09:00:00', '2024-04-22');

--Billing table
INSERT INTO Billing (memberID, amount, payFor) VALUES
(1, 20.00, 'Membership Fee'),
(2, 20.00, 'Membership Fee'),
(1, 50.00, 'Personal Training'),
(2, 50.00, 'Personal Training');

--Admins table
INSERT INTO Admins (email, pass, adminName) VALUES
('admin@example.com', 'adminpass', 'Admin User');

--Equipment table
INSERT INTO Equipment (equipName, lastMaintenance, nextMaintenance) VALUES
('Treadmill', '2023-05-20', '2024-05-20'),
('Rowing Machine', '2024-03-15', '2024-09-15');

