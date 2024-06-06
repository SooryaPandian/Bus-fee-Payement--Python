import datetime
import random  # for generating random numbers

# Function to create a new transaction ID
def create_transaction_id(rollno):

    # Generate a timestamp with current date and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Extract the last three digits of the roll number
    rollno_last_three = rollno[-3:]

    # Generate a random number between 100 and 999
    random_number = random.randint(100, 999)

    # Combine timestamp, date, and last three digits of the roll number to create the transaction ID
    transaction_id = f"{timestamp}_{rollno_last_three}_{random_number}"

    return transaction_id
