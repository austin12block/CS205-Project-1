import sqlite3
from sqlite3 import Error

#SQL Instructions:
def createSQLConnection():
    try:
        # connect to the database
        connectSQLite = sqlite3.connect('topSpotifySongs.db')

        # create database table here
        # TODO: Finish filling in table with fields
        createTable = '''CREATE TABLE TopSpotifySongs (
                      Artist INTEGER PRIMARY KEY);'''

        # create cursor object which will be used for queries
        cursor = connectSQLite.cursor()
        print('Connected to SQLite')

        # commit the table
        cursor.execute(createTable)
        connectSQLite.commit()
        print('Table for Spotify songs was created!')

        # close cursor object
        cursor.close()

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)

def main():
    # establish SQLite connection
    createSQLConnection()
    
    #test
    userCommand = input("Enter a command: ")

    interpretCommand(userCommand)

def interpretCommand(userCommand):
    pass
    #Pseudocode:
    #Extract whatever the first word is of the command, split @ first space
    #Use switch statement to choose which command, or SQL stuff?

main()