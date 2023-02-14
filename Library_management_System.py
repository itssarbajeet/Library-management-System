#code by AYUSH
import csv
import ssl
import smtplib
def send_email(to ,serial_number, cost_per_day, days_of_rent):
    from_email = "teamalphacgu@gmail.com" #use your mail
    password ="sunyczlllwfmdcoy"  #should be 2 step verified and use app password here
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    subject = "Book Rental Details"
    context = ssl.create_default_context()

    # Binding Subject and body
    body="THANKS FOR RENTING BOOKS FROM OUR LIBRARY"
    body += "\nBook Serial Number: {}\n".format(serial_number)
    body += "Rental Period: {} days\n".format(days_of_rent)
    body += "Total Cost: {}\n".format(cost_per_day * days_of_rent)
    message = "Subject: {}\n\n{}".format(subject, body)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(from_email, password)
            server.sendmail(from_email, to, message)
    except Exception as e:
        print("Failed to send email:", e)

# Function to add a book to the book.csv file
def add_book(book_name, book_serial, rented):
  # Open the book.csv file in append mode
  with open('book.csv', 'a', newline='') as csv_file:
    # Create a writer object
    writer = csv.writer(csv_file)
    # Add the book details as a row in the CSV file
    writer.writerow([book_name, book_serial, rented])
  print("Book added successfully!")

#  To add a user to the user.csv file
def add_user(name, email, phone):
  # Open the user.csv file in append mode
  with open('user.csv', 'a', newline='') as csv_file:
    # Create a writer object
    writer = csv.writer(csv_file) 
    # Add the user details as a row in the CSV file
    writer.writerow([name, email, phone, "", 0, 0])
  print("User added successfully!")

def rent_book(book_serial, email, cost_per_day, days_of_rent,serial_number):
  # Check if the user with the given email is present in the user.csv file
  user_exists = False
  with open('user.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      if row[1] == email:
        user_exists = True
        break
  if not user_exists:
    print("User does not exist in our database")
    print("Please Add the user before renting the book")
    return
  # Check if the book with the given serial number exists in the book.csv file
  book_exists = False
  with open('book.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      if row[1] == book_serial:
        book_exists = True
        break
  if not book_exists:
    print("Book not found")
    return
  # Set the rented book status of the book to 1 (rented)
  update_book_status(book_serial, 1)
  # Update the user's rented book and rent details in the user.csv file
  update_user_rent_details(email, book_serial, cost_per_day, days_of_rent)

  send_email(email, serial_number, cost_per_day, days_of_rent)
  return "Book rented successfully"

# Function to return a book
def return_book(email):
  # Read the user.csv file to get the details of the user with the given email
  with open('user.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      if row[1] == email:
        # Get the book serial number and rent details of the user
        book_serial = row[3]
        cost_per_day = float(row[4])
        days_of_rent = int(row[5])
        break
  # Calculate the rent amount
  rent_amount = cost_per_day * days_of_rent
  # Set the rented status of the book to 0 (not rented)
  update_book_status(book_serial, 0)
  # Update the user's rented book and rent details in the user.csv file
  update_user_rent_details(email, "", 0, 0)
  print("Book returned successfully! Total rent amount: {}".format(rent_amount))
# Function to delete a book from the book.csv file
def delete_book(book_serial):
  # Read the book.csv file
  with open('book.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    # Create a list to store the rows of the file
    rows = []
    for row in reader:
      # If the row represents the book to be deleted, skip it
      if row[1] != book_serial:
        rows.append(row)
  # Write the modified list of rows to the book.csv file
  with open('book.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(rows)
  print("Book deleted successfully!")

# Function to delete a user from the user.csv file
def delete_user(email):
  # Read the user.csv file
  with open('user.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    # Create a list to store the rows of the file
    rows = []
    for row in reader:
      # If the row represents the user to be deleted, skip it
      if row[1] != email:
        rows.append(row)
  # Write the modified list of rows to the user.csv file
  with open('user.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(rows)
  print("User deleted successfully!")

# Helper function to update the rented status of a book in the book.csv file
def update_book_status(book_serial, rented):
  # Read the book.csv file
  with open('book.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    # Create a list to store the rows of the file
    rows = []
    for row in reader:
      # If the row represents the book to be updated, update the rented status
      if row[1] == book_serial:
        row[2] = rented
      rows.append(row)
  # Write the modified list of rows to the book.csv file
  with open('book.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(rows)

# Helper function to update the rented book and rent details of a user in the user.csv file
def update_user_rent_details(email, book_serial, cost_per_day, days_of_rent):
  # Read the user.csv file
  with open('user.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    # Create a list to store the rows of the file
    rows = []
    for row in reader:
      # If the row represents the user to be updated, update the rented book and rent details
      if row[1] == email:
        row[3] = book_serial
        row[4] = cost_per_day
        row[5] = days_of_rent
      rows.append(row)
  # Write the modified list of rows to the user.csv file
  with open('user.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(rows)

# Main function to run the library management system
def run_library_system():
  while True:
    # Print the options
    print("[1] Add a book")
    print("[2] Add a user")
    print("[3] Rent a book")
    print("[4] Return a book")
    print("[5] Delete a book")
    print("[6] Delete a user")
    print("[7] Exit")
    # Get the user's choice
    choice = input("Enter your choice: ")
    if choice == "1":
      # Add a book
      book_name = input("Enter the book name: ")
      book_serial = input("Enter the book serial number: ")
      add_book(book_name, book_serial, 0)
    elif choice == "2":
      # Add a user
      name = input("Enter the name: ")
      email = input("Enter the email: ")
      phone = input("Enter the phone number: ")
      add_user(name, email, phone)
    elif choice == "3":
      # Rent a book
      book_serial = input("Enter the book serial number: ")
      email = input("Enter the email: ")
      cost_per_day = float(input("Enter the cost per day: "))
      days_of_rent = int(input("Enter the number of days of rent: "))
      
      rent_book(book_serial, email, cost_per_day, days_of_rent,book_serial)
    elif choice == "4":
      # Return a book
      email = input("Enter the email: ")
      return_book(email)
    elif choice == "5":
      # Delete a book
      book_serial = input("Enter the book serial number: ")
      delete_book(book_serial)
    elif choice == "6":
      # Delete a user
      email = input("Enter the email: ")
      delete_user(email)
    elif choice == "7":
      # Exit the system
      break
    else:
      print("Invalid choice")

# Run the library management system
run_library_system()