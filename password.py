import sqlite3
from sys import exit
from time import sleep





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

while (True):
    print("*" * 5)
    print("MEMU")
    print("q: Quit")
    print("l: List entries")
    print("a: Add entry")
    print("u: Update entry")
    print("r: Remove entry")
    print("*" * 5)

    command = input(": ")
    if command == "q":
        exit()
    elif command == "l":
        for row in db.execute("SELECT * FROM passwords"):
            print("service | username | password")
            print(row, sep=" | ")
            sleep(10)
    elif command == "a":
        service = input("Service: ")
        username = input("Username: ")
        password = input("Password: ")
        db.execute("INSERT INTO passwords (service, userName, password) VALUES (?, ?, ?)", (service, username, password))
        print("Success!")
        sleep(.5)
    elif command == "u":
        exit()
    elif command == "r":
        exit()
    else:
        print("Invalid command -- try again")
        sleep(1)