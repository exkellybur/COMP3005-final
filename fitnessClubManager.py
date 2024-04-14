import psycopg2

def db_connect():
    try: 
        conn = psycopg2.connect(
            dbname="hfclub",
            user="postgres",
            password="3005",
            host="localhost",
            port="5432"
        )
        #print("Connected to the database!")
        return conn
    except psycopg2.Error as e:
        print(f"Unable to connect to the database: {e}")
        return None

# Function to execute all queries 
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        if "RETURNING" in query:
            return cursor.fetchone()[0]# Return the fetched value
        conn.commit()
        cursor.close()
        print("Query executed successfully")
    except Exception as e:
        print(f"Error executing query: {e}")

#function for trainers to add availability
def add_avail(trainerID):
        print("Please provide a time slot for your availability.")
        day = input("Enter date (YYYY-MM-DD): ")
        startTtime = input("Enter start time (00:00:00): ")
        endTime = input("Enter end time (00:00:00): ")

        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Availability(trainerID, startTime, endTime, availDate) VALUES (%s, %s, %s, %s)", (trainerID, startTtime, endTime, day))
        conn.commit()
        conn.close()

#function to insert a new member into the table 
def insert_member(email, password, name, gender, height, weight, muscle_mass):
    conn = db_connect()
    cursor = conn.cursor()
    #query to add member
    cursor.execute("INSERT INTO Members(email, pass, memberName, gender) VALUES (%s, %s, %s, %s) RETURNING memberID", (email, password, name, gender))
    userID = cursor.fetchone()[0] # retrieve memberID
    print("UserID: ")
    print(userID)
    #query to insert health metrics of member
    cursor.execute("INSERT INTO HealthMetrics (memberID, height, weight, muscleMass) VALUES (%s, %s, %s, %s)", (userID, height, weight, muscle_mass))
    conn.commit()
    conn.close()
    return userID

#for inserting trainers and admins
def insert_staff(email, password, name, role):
    conn = db_connect()
    cursor = conn.cursor()
    #query to add user to appropriate table
    table = role + "s"
    username = role + "Name"
    returnID = role + "ID"
    cursor.execute("INSERT INTO %s(email, pass, %s) VALUES (%s, %s, %s) RETURNING %d", (table, username, email, password, name, returnID))
    userID = cursor.fetchone()[0] # retrieve memberID
    conn.commit()
    conn.close()
    return userID

#function to register user 
def signup():
    #ask for basic user information 
    print("\n---REGISTERING NEW USER---")
    print("Please input the following information.")
    email = input("Enter email: ")
    password = input("Enter password: ")
    name = input("Enter name: ")
    role = input("Choose user type (member/trainer/admin): ") #ask for type of user 

    #if user choosed member type 
    if role.lower() == "member":
        print("Please complete the following information to register as a member.")
        gender = input("Enter gender (M/F): ")
        height = int(input("Enter height (in cm): "))
        weight = int(input("Enter weight (in kg): "))
        muscle_mass = int(input("Enter muscle mass (in kg): "))
        userID = insert_member(email, password, name, gender, height, weight, muscle_mass) #add a member
        print("Successfully registered as a member!")
        return [str(userID), role + "s"]

    #if user chooses trainer type
    elif role.lower() == "trainer":
        #query to add trainer first so we can retrieve trainerID for availability
        userID = insert_staff(email, password, name, role)

        print("Finish registering as a trainer by providing a time slot for your availability.") #get availability
        add_avail(userID)

        print("Successfully registered as a trainer!")
        return [str(userID), role +"s"]
        

    elif role.lower() == "admin":
        # add_admin = "INSERT INTO Admin(email, pass, adminName) VALUES (%s, %s, %s)", (email, password, name)
        userID = insert_staff(email, password, name, role)
        print("Successfully registered as an admin!")
        return [str(userID), role +"s"]
    else:
        print("Invalid User type")
        return ["none", "none"]

#function to authenticate user login 
def login():
    print("\n---LOGIN PAGE---")
    email = input("Enter email: ")
    password = input("Enter password: ")

    conn = db_connect()
    cursor = conn.cursor()

    #check member table
    cursor.execute("SELECT memberID, pass FROM Members WHERE email = %s", (email,))
    member = cursor.fetchone()
    #check trainer table 
    cursor.execute("SELECT trainerID, pass FROM Trainers WHERE email = %s", (email,))
    trainer = cursor.fetchone()
    #check admin table
    cursor.execute("SELECT adminID, pass FROM Admins WHERE email = %s", (email,))
    admin = cursor.fetchone()

    if member is not None and member[1] == password:
        return [member[0], "members"]
    elif trainer is not None and trainer[1] == password:
        return [trainer[0], "trainers"]
    elif admin is not None and admin[1] == password:
        return [admin[0], "admins"]
    else:
        print("Authentication failed: Incorrect email/password or user is not registered.")
        return ["none", "none"]; 
    

#function to choose correct menu to display for user 
def generate_menu(currUser):
    #display appropraite prompts according to user type 
    if currUser[1] == "members":
        display_member_menu(currUser[0])
    elif currUser[1] == "trainers":
        display_trainer_menu(currUser[0])
    else:
        display_admin_menu(currUser[0])

def display_member_menu(memberID):
    while True:
        print("\n---MEMBER MENU---")
        print("Please select what you would like to do: ")
        print("1. Update Health Metrics")
        print("2. Add Fitness Goal")
        print("3. Display your Dashboard")
        print("4. Sign up for a group class")
        print("5. Book a Personal Training Session")
        print("6. Logoff / Quit program")

        selection = input("Enter selection number: ")
        if selection == "1":
            update_metrics(memberID)
        elif selection == "2":
            add_goal(memberID)
        elif selection == "3":
            display_dashboard(memberID)
        elif selection == "4":
            register_class(memberID)
        elif selection == "5":
            book_session(memberID)
        elif selection == "6":
            break
        else:
            print("Invalid selection.")

def update_metrics(memberID):
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---UPDATE YOUR HEALTH METRICS---")
    height = int(input("Enter height (in cm): "))
    weight = int(input("Enter weight (in kg): "))
    muscle_mass = int(input("Enter muscle mass (in kg): "))

    cursor.execute("UPDATE HealthMetrics SET height = %s, weight = %s, muscleMass = %s WHERE memberID = %s", (height, weight, muscle_mass, memberID))
    conn.commit()
    print("Health metrics updated successfully!")
    conn.close()

def add_goal(memberID):
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---ADD A FITNESS GOAL---")
    weight = int(input("Enter goal weight (in kg): "))
    date = input("Enter goal date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO FitnessGoals (memberID, goalWeight, goalDate) VALUES (%s, %s, %s)", (memberID, weight, date))
    conn.commit()
    print("Fitness goal added successfully!")
    conn.close()


#function that displays given members information - their "dashboard" 
def display_dashboard(memberID):
    conn = db_connect()
    cursor = conn.cursor()

    #query for member's health metrics 
    cursor.execute("SELECT height, weight, muscleMass FROM HealthMetrics WHERE memberID = %s", (memberID,))
    health_metrics = cursor.fetchone()
    print("\n---DISPLAYING MEMBER DASHBOARD---")
    print("Health Metrics:")
    print(f"Height: {health_metrics[0]} cm")
    print(f"Weight: {health_metrics[1]} kg")
    print(f"Muscle Mass: {health_metrics[2]} kg")

    #query for routines 
    cursor.execute("SELECT description FROM Routines WHERE memberID = %s", (memberID,))
    routines = cursor.fetchall()
    print("\nRoutines:")
    for routine in routines:
        print(routine[0])

    #query member's fitness goals
    cursor.execute("SELECT goalWeight, goalDate FROM FitnessGoals WHERE memberID = %s", (memberID,))
    fitness_goals = cursor.fetchall()
    print("\nFitness Goals:")
    for goal in fitness_goals:
        print(f"Goal Weight: {goal[0]} kg, Goal Date: {goal[1]}")
    
    conn.close()

#function that displays all the available group classes 
def register_class(memberID):
    conn = db_connect()
    cursor = conn.cursor()
    print("\n---GROUP CLASS REGISTRATION---")
    #query for classes
    cursor.execute("SELECT classID, className, startTime, endTime, classDay FROM GroupClasses")
    classes = cursor.fetchall()
    for classInfo in classes:
            classID, className, startTime, endTime, classDay = classInfo
            print(f"Class ID: {classID}, Name: {className}, Time: {startTime} - {endTime}, Day: {classDay}")

    selection = int(input("Enter desired Class ID (or type 'cancel' to go back): "))
    if selection == "cancel":
        return
    else: #register
        cursor.execute("INSERT INTO ClassRegistrations (memberID, classID) VALUES (%s, %s)",(memberID, selection))
        conn.commit()
        print("Successfully registered for the class!")
        conn.close()

        #create a billing for the class
        cursor.execute("INSERT INTO Billing (memberID, amount, payFor) VALUES (%s, %s, %s)", (memberID, 35.00, 'Group Class Registration'))
        conn.commit()
        print("Billing created for registration.")
    conn.close()

def book_session():
    print("\n---BOOK A PERSONAL SESSION---")
    


def display_trainer_menu(trainerID):
    while True:
        print("\n---TRAINER MENU---")
        print("Please select what you would like to do: ")
        print("1. Add availability")
        print("2. Search members")
        print("3. View sessions")
        print("4. Logoff / Quit program")

        selection = input("Enter selection number: ")
        if selection == "1":
            add_avail(trainerID)
        elif selection == "2":
            search_members()
        elif selection == "3":
            display_sessions(trainerID)
        elif selection == "4":
            break
        else:
            print("Invalid selection.")

#fucntion that allows trainers to search members by name
def search_members():
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---MEMBER PROFILE VIEWING---")
    search = input("Enter name of member: ")
    #search for all members with matching name 
    cursor.execute("SELECT memberName, gender, memberID FROM Members WHERE memberName LIKE %s", ('%' + search + '%',))
    members = cursor.fetchall()

    if members is not None:
        for member in members:
            print("\nSearch Results:")     
            memberName, gender, memberID = member
            print(f"\nName: {memberName}")
            print(f"Gender: {gender}")

            #get members health metrics
            cursor.execute("SELECT height, weight, muscleMass FROM HealthMetrics WHERE memberID = %s", (memberID,))
            health_metrics = cursor.fetchone()
            height, weight, muscle_mass = health_metrics
            print("Health Metrics:")
            print(f"Height: {height} cm")
            print(f"Weight: {weight} kg")
            print(f"Muscle Mass: {muscle_mass} kg")

    else:
        print("No members found with that name.")

#function that displays all group classes and personal sessions that the trainer is holding 
def display_sessions(trainerID):
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---DISPLAYING SESSIONS---")

    #find trainers group classes
    cursor.execute("SELECT className, startTime, endTime, classDay FROM GroupClasses WHERE trainerID = %s", (trainerID,))
    group_classes = cursor.fetchall()
    if group_classes is not None:
        print("\nGroup Classes:")
        for aclass in group_classes:
            className, startTime, endTime, classDay = aclass
            print(f"Class Name: {className}")
            print(f"Class Day: {classDay}")
            print(f"Start Time: {startTime}")
            print(f"End Time: {endTime}")
    else:
        print("No group classes scheduled for this trainer.")

    #find all personal sessions for this trainer
    cursor.execute("SELECT startTime, endTime, sessionDay FROM PersonalSessions WHERE trainerID = %s", (trainerID,))
    personalSessions = cursor.fetchall()

    if personalSessions is not None:
        print("\nPersonal Sessions:")
        for session in personalSessions:
            startTime, endTime, sessionDay = session
            print(f"Session Day: {sessionDay}")
            print(f"Start Time: {startTime}")
            print(f"End Time: {endTime}")
    else:
        print("No personal sessions scheduled for this trainer.")

    conn.close()



def display_admin_menu(adminID):
    while True:
        print("\n---ADMIN MENU---")
        print("Please select what you would like to do: ")
        print("1. Manage rooms")
        print("2. Monitor Equipment")
        print("3. Update class schedules")
        print("4. Process billings")
        print("5. Logoff / Quit program")

        selection = input("Enter selection number: ")
        if selection == "1":
            manage_rooms()
        elif selection == "2":
            monitor_equipment()
        elif selection == "3":
            update_classes()
        elif selection == "4":
            process_billings()
        elif selection == "5":
            break
        else:
            print("Invalid selection.")

#function that displays all rooms 
def manage_rooms():
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---MANAGE ROOMS---")
    #get all rooms 
    cursor.execute("SELECT roomID, roomName, booked FROM Rooms")
    rooms = cursor.fetchall()
    if rooms is not None:
        print("\nRooms:")
        for room in rooms:
            roomID, roomName, booked = room
            print(f"Room Name: {roomName}")
            print(f"Booked: {'Yes' if booked else 'No'}")

            #if room is booked, display the group class that booked it 
            if booked:
                cursor.execute("SELECT className FROM GroupClasses WHERE roomID = %s", (roomID,))
                classes = cursor.fetchall()
                print("Booked by: " + classes[0])
    else:
        print("No rooms found.")

#function for admin to create classes
def update_classes():
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---CREATE GROUP CLASSES---")

    conn.close()

#function for admin to create monitor equipment
def monitor_equipment():
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---MONITOR EQUIPMENT---")

    # get all equipment
    cursor.execute("SELECT * FROM Equipment")
    equipment = cursor.fetchall()
    print("\nEquipment:")
    for e in equipment:
        equipID, equipName, lastMaintenance, nextMaintenance = e
        print(f"\nEquipment Name: {equipName}")
        print(f"Last Maintenance: {lastMaintenance}")
        print(f"Next Maintenance: {nextMaintenance}")

    conn.close()

#function for admin to process bills 
def process_billings():
    conn = db_connect()
    cursor = conn.cursor()

    print("\n---PROCESS BILLINGS---")

    # get all billings
    cursor.execute("SELECT * FROM Billing")
    billings = cursor.fetchall()
    print("\nBillings:")
    for billing in billings:
        billingID, memberID, amount, payFor = billing
        print(f"\nBilling ID: {billingID}")
        print(f"Member ID: {memberID}")
        print(f"Amount: ${amount}")
        print(f"Payment For: {payFor}")

    conn.close()

def main():
    conn = db_connect()
    currUser = [] #stores current user info in this format - [userID, table (members, trainers, admins)]
    if conn is not None:
        while True:
            print("\nMake a selection:")
            print("1. Log in")
            print("2. Sign Up")
            print("3. Exit")

            selection = input("Enter selection number: ")

            #log in 
            if selection == "1":
                currUser = login();
                # print("logged in as: ")
                # print(currUser)   
                if currUser[1] != "none":
                    generate_menu(currUser)
                    break

            #sign up
            elif selection == "2":
                currUser = signup();
                if currUser[0] != "none":
                    generate_menu(currUser)
                    break
                
            #exit
            elif selection =="3":
                break
            else: 
                print("Invalid Selection.")
        

if __name__ == "__main__":
    main()