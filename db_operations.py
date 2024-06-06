import mysql.connector

# Function to connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='soorya',
            database='busfee'
        )
        print("Database connected successfully")
        return conn
    except Exception as e:
        print("Error connecting to database:", str(e))
        raise

# Function to check if a user exists in the database
def user_exists(rollno, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE rollno=%s AND password=%s", (rollno, password))
    user = cur.fetchone()
    conn.close()
    return user

# Function to add a new user to the database
def add_user(rollno, password, firstname, lastname, email, busnumber, busstop):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user (rollno, password, firstname, lastname, email, busnumber, busstop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (rollno, password, firstname, lastname, email, busnumber, busstop))
    conn.commit()
    conn.close()

# Function to fetch user details by roll number
def fetch_user_details(rollno):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE rollno = %s", (rollno,))
    user_details = cur.fetchone()
    conn.close()
    return user_details

# Function to update user status
def update_user_status(rollno):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE user SET stat = TRUE WHERE rollno = %s", (rollno,))
        conn.commit()
        conn.close()
        print(f"User status updated for rollno {rollno}")
    except Exception as e:
        print("Error updating user status:", str(e))

# Function to fetch students based on filtering options
def fetch_students(bus_number_filter=None, paid_status_filter=None):
    conn = connect_db()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM user WHERE 1"
    params = []

    if bus_number_filter:
        query += " AND busnumber = %s"
        params.append(bus_number_filter)

    if paid_status_filter == "paid":
        query += " AND stat = 1"
    elif paid_status_filter == "not_paid":
        query += " AND stat = 0"

    cur.execute(query, params)
    students = cur.fetchall()

    conn.close()
    return students
def fetch_transaction_details(rollno):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE rollno = %s", (rollno,))
    transaction_details = cur.fetchall()
    conn.close()
    return transaction_details

def update_user_status(rollno,transaction_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE user SET stat = TRUE WHERE rollno = %s", (rollno,))
        cur.execute("UPDATE transactions SET status = TRUE WHERE transaction_id = %s", (transaction_id,))
        print(f"updated status for the transaction id :{transaction_id}")
        conn.commit()
        conn.close()
        print(f"User status updated for rollno {rollno}")
    except Exception as e:
        print("Error updating user status:", str(e))


def fetch_all_bus_details():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM busdetails")
    bus_details = cur.fetchall()
    conn.close()
    return bus_details



def fetch_bus_numbers():
    conn = connect_db()
    cur = conn.cursor()

    # Execute query to fetch unique bus numbers
    cur.execute("SELECT DISTINCT busnumber FROM user")
    bus_numbers = [row[0] for row in cur.fetchall()]  # Extracting the first element of each row
    print(bus_numbers)
    conn.close()
    return bus_numbers

def fetch_bus_detailss(busno,stop):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM busdetails WHERE busnumber=%s AND busstop=%s", (busno, stop))
    bus = cur.fetchone()
    conn.close()
    return bus

def fetch_bus_details(bus_number):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM busdetails WHERE busnumber= %s", (bus_number,))
    bus_details = cur.fetchall()
    conn.close()
    print(bus_details,bus_number,end=" ")
    return bus_details

def fetch_students(bus_number_filter=None, paid_status_filter=None):
    print("In fetch_students",bus_number_filter,paid_status_filter)
    conn = connect_db()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM user WHERE 1"
    params = []

    if bus_number_filter:
        query += " AND busnumber = %s"
        params.append(bus_number_filter)

    if paid_status_filter == "paid":
        query += " AND stat = 1"
    elif paid_status_filter == "not_paid":
        query += " AND stat = 0"

    cur.execute(query, params)
    students = cur.fetchall()

    conn.close()
    return students
