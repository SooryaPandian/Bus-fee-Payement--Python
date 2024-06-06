from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from transactionId import create_transaction_id
from db_operations import *
app = Flask(__name__)
app.secret_key = 'ehorizon project'


transactionId= "None"
@app.route("/show_transport", methods=["GET", "POST"])
def bus_details():
    # Fetch bus numbers from the busdetails table
    bus_numbers = fetch_bus_numbers()

    # Fetch bus details based on filtering options
    if request.method == "POST":
        bus_number_filter = request.form.get("bus_number")
        if bus_number_filter:
            bus_details = fetch_bus_details(bus_number_filter)
        else:
            bus_details = fetch_all_bus_details()
    else:
        print("fetched all bus details")
        bus_details = fetch_all_bus_details()
    print("These are the bus details", bus_details)
    return render_template("transport.html", bus_numbers=bus_numbers, bus_details=bus_details)

@app.route('/transport')
def transport():
    return render_template('transport.html')
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        rollno = request.form["rollno"]
        password = request.form["password"]
        user = user_exists(rollno, password)
        if user:
            # Store user information in session
            session['rollno'] = rollno
            session['firstname'] = user[2]  # Assuming the firstname is stored at index 2
            session['stat'] = user[6]

            # Fetch user details
            user_details = fetch_user_details(rollno)

            # Fetch bus details
            bus_details = fetch_bus_detailss(user_details[7], user_details[8])
            print("The bus details of the student",bus_details)
            if bus_details:
                amount = bus_details[2]  # Assuming 'amount' is the column name for the amount in bus_details
                session['amount'] = amount
                print("The amount is ",amount)
            else:
                # If bus details not found, set amount to 0 or any default value
                session['amount'] = 0

            print(user[6])
            return render_template("home.html", user_details=user_details)
        else:
            error = "Invalid credentials. Please try again."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/facility")
def facility():
    return  render_template("busfacility.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        rollno = request.form.get("rollno")
        password = request.form.get("password")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        busno = request.form.get("busnumber")  # Change 'busno' to 'busnumber'
        busstop = request.form.get("busstop")

        # Check if any required field is missing
        if None in [rollno, password, firstname, lastname, email, busno, busstop]:
            error_message = "One or more required fields are missing."
            return render_template("login.html", error=error_message)

        try:
            add_user(rollno, password, firstname, lastname, email, busno, busstop)
            session['rollno'] = rollno
            return redirect(url_for("home"))
        except Exception as e:
            error_message = "Error occurred while registering user: {}".format(str(e))
            return render_template("login.html", error=error_message)
    return render_template("login.html")

# Function to update the status field in the user table

@app.route("/payment_success", methods=["POST"])
def payment_success():
    print("payment_success called")
    try:
        data = request.get_json()
        payer_name = data.get("payerName")
        # Retrieve the rollno from the session
        rollno = session.get("rollno")
        # Process the success message and update the user status
        if rollno:
            update_user_status(rollno,globals()['transactionId'])
            transactionId= "None"
        print(f"Payment successful for {payer_name}")
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error processing payment success:", str(e))
        return jsonify({"status": "error"})


# Route for creating a new transaction ID and storing transaction details
@app.route("/create_transaction_id", methods=["GET"])
def create_transaction_id_endpoint():
    print("create_transaction_id_endpoint called")
    try:
        print("create_transaction_id_endpoint called in try block")
        # Retrieve rollno from session
        rollno = session.get("rollno")
        print(rollno)
        if not rollno:
            return jsonify({"error": "Roll number not found in session"}), 400

        # Generate transaction ID
        transaction_id = create_transaction_id(rollno)
        print("transction id is"+transaction_id)
        globals()['transaction_id']=transaction_id
        # Add transaction details to the database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (transaction_id, rollno, amount, status) VALUES (%s, %s, %s, %s)",
                    (transaction_id, rollno, 10, False))  # Assuming amount is 10 and status is initially False
        conn.commit()
        conn.close()

        return jsonify({"transaction_id": transaction_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/home")
def home():
    rollno = session.get("rollno")
    if rollno:
        user_details = fetch_user_details(rollno)
        return render_template("home.html", user_details=user_details)
    else:
        # Redirect to login if the roll number is not available in the session
        return redirect(url_for("login"))
@app.route("/payment")
def payment():
    rollno = session.get("rollno")
    if rollno:
        user_details = fetch_user_details(rollno)
        session['stat'] = user_details[6]
        transaction_details = fetch_transaction_details(rollno)  # Fetch transaction details
        print(transaction_details)
        return render_template("payment.html", user_details=user_details, transaction_details=transaction_details)
    else:
        # Redirect to login if the roll number is not available in the session
        return redirect(url_for("login"))
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")



# Fetch students based on filtering options


# Fetch unique bus numbers from the users table


# Function to handle the admin panel route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Fetch bus numbers from the busdetails table
    bus_numbers = fetch_bus_numbers()

    # Fetch students data based on filtering options
    if request.method == "POST":
        bus_number_filter = request.form.get("bus_number")
        paid_status_filter = request.form.get("paid_status")
        print("deatils from the form ", bus_number_filter, paid_status_filter,end=" ")
        students = fetch_students(bus_number_filter, paid_status_filter)
    else:
        students = fetch_students()
        print("THE STUDENT LIST :",students)
    return render_template("admin.html", bus_numbers=bus_numbers, students=students)
@app.route("/student_get", methods=["GET", "POST"])
def student():
    # Fetch students data based on filtering options
    if request.method == "POST":
        rollno = request.form.get("roll_number")

        print(rollno)
        student = fetch_user_details(rollno)

    return render_template("student.html",student=student)
@app.route("/student")
def detail():
    return render_template('student.html')
if __name__ == "__main__":
    app.run(debug=True)
