import sqlite3
from sys import exit
from time import sleep
import secrets
import string
import re
import os


def main():
    # Default admin password
    adminPassword = preLogin()


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
            db.close()
            print("Saving changes...")
            sleep(.5)
            print("Exiting\nThank you!")
            exit()
        # Searches current database
        elif command == "s":
            search = input("Which service are you looking for: ")
            for row in db.execute("SELECT * FROM passwords WHERE service=?;", (search,)):
                    print("--- {row}")
            pressEnter()

        # Lists all entries in database
        elif command == "l":
            print("--- (Service, Username, Password)")
            for row in db.execute("SELECT * FROM passwords"):
                    print(f"--- {row}")
            pressEnter()
        # Adds entry to database
        elif command == "a":
            service = input("Service: ")
            username = input("Username: ")

            # Gives user chance to generate secure password
            secure = input("Would you like to generate a secure password (y | n):")
            if re.search("^y(es)?$", secure, re.IGNORECASE):
                password = makePassword()
                print(f"Your secure password is: {password}")
            elif re.search("^n(o)?$", secure, re.IGNORECASE):
                password = input("Password: ")
            
            # Adds new entry to database
            db.execute("INSERT INTO passwords (service, userName, password) VALUES (?, ?, ?)", (service.lower(), username, password))
            print("Successfully added entry")
            pressEnter()
        
        # Updates specified entry
        elif command == "u":
            search = input("Which service are looking for: ")

            # Gives user chance to generate secure password
            secure = input("Would you like to generate a secure password (y | n):")
            if re.search("^y(es)?$", secure, re.IGNORECASE):
                newPW = makePassword()
                print(f"Your secure password is: {newPW}")
            elif re.search("^n(o)?$", secure, re.IGNORECASE):
                newPW = input("What is your new password: ")

            # Updates specified entry
            db.execute("UPDATE passwords SET password=? WHERE service=?;", (newPW, search.lower()))
            print("Successfully updated!")
            pressEnter()

        # Removes specified entry
        elif command == "r":
            removal = input("Which service do you want to remove:")
            db.execute("DELETE FROM passwords WHERE service=?;", (removal.lower(),))
            print("Successfully removed!")
            pressEnter()

        # If user enters invalid command
        else:
            print("Invalid command -- try again")
            pressEnter()

def preLogin ():
    admin = "12345"
    config = "config.ini"
    # if credentials config is absent
    if config not in os.listdir(path="."):
        print("CREDENTIALS NOT FOUND")
        sleep(.5)
        with open(config, "w") as file:
            password = input("New user! Create an admin password: ")
            file.write(password)
            admin = password
            print("Thank you! Don't forget your password.")
            sleep(.5)

    # if credentials config is present
    else:
        print("CREDENTIALS FOUND")
        with open(config, "r") as file:
            password = file.read()
            admin = password
    return admin


def makePassword():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
            break
    return password

def pressEnter():
    input("Press Enter to continue...")

main()