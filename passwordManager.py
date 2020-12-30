import sqlite3
from sys import exit
from time import sleep
import secrets
import string

# Default admin password
adminPassword = "12345"

# Initial admin login prompt
login = input("Admin password: ")
if login == "q":
    print("Quitting...")
    sleep(.5)
    exit()

# Check that supplied password matches admin
while login != adminPassword:
    login = input("Admin password: ")
    if login == "q":
        print("Quitting...")
        sleep(.5)
        exit()

# Connect to database or creates w/ table on on failure
db = sqlite3.connect("password.db")
try:
    db.execute(
         """CREATE TABLE passwords (
        service TEXT, 
        userName TEXT,
        password TEXT);""")
    print("New database created!\nWhat would you like to do?")
except:
    print("Thanks for logging in!\nWhat would you like to do?")

# Main loop of program
while (True):
    print("*" * 10)
    print("* MEMU:")
    print("* q: Quit")
    print("* s: Search entries")
    print("* l: List entries")
    print("* a: Add entry")
    print("* u: Update entry")
    print("* r: Remove entry")
    print("*" * 10)

    command = input(": ")
    if command == "q":
        db.commit()
        print("Saving changes...")
        sleep(.5)
        print("Exiting\nThank you!")
        exit()
    # Searches current database
    elif command == "s":
        search = input("Which service are you looking for: ")
        for row in db.execute("SELECT * FROM passwords WHERE service=?;", (search,)):
            print(row)
    # Lists all entries in database
    elif command == "l":
        for row in db.execute("SELECT * FROM passwords"):
            print(row)
    # Adds entry to database
    elif command == "a":
        service = input("Service: ")
        username = input("Username: ")
        password = input("Password: ")
        db.execute("INSERT INTO passwords (service, userName, password) VALUES (?, ?, ?)", (service.lower(), username, password))
        print("Success!")
        sleep(.5)
    # Updates specified entry
    elif command == "u":
        search = input("Which service are looking for: ")
        newPW = input("What is your new password: ")
        db.execute("UPDATE passwords SET password=? WHERE service=?;", (newPW, search.lower()))
    # Removes specified entry
    elif command == "r":
        removal = input("Which password do you want to remove:")
        result = db.execute("DELETE FROM passwords WHERE service=?;", (removal.lower(),))
        if result == 0:
            print("Entry not found. Try again.")
    # If user enters invalid command
    else:
        print("Invalid command -- try again")
        sleep(1)