import sqlite3, csv
from sqlite3 import Error

# SQL Instructions:
def querySQL(unknownField, knownField, knownFieldValue):
    unknownField = unknownField.lower()
    knownField = knownField.lower()
    knownFieldValue = knownFieldValue.lower()
    try:
        # connect to the database
        connectSQLite = sqlite3.connect('SpotifyData.db')

        # create cursor object which will be used for queries
        cursor = connectSQLite.cursor()

        # switch statement for knownField to help create query statement
        if knownField == "artist" or knownField == "birthdate" or knownField == "hometown":
            knownFieldAppended = "artists." + knownField
        elif knownField == "song" or knownField == "genre":
            knownFieldAppended = "songs." + knownField
        else:
            return "Could not complete query for " + knownField + " field"

        # switch statement for unknownField to help create query statement
        if unknownField == "artist" or unknownField == "birthdate" or unknownField == "hometown":
            unknownFieldAppended = "artists." + unknownField
        elif unknownField == "song" or unknownField == "genre":
            unknownFieldAppended = "songs." + unknownField
        else:
            return "Could not complete query for " + unknownField + " field"

        # create query
        query = "SELECT DISTINCT " + unknownFieldAppended + " FROM songs INNER JOIN artists ON songs.artist = artists.artist WHERE " + knownFieldAppended + "='" + knownFieldValue + "' COLLATE NOCASE"

        # execute the query and get the needed information from the database
        cursor.execute(query)
        rows = cursor.fetchall()

        queryString = ''
        # go through each row of returned field to get the unknown values
        for row in rows:
            # create return string from query
            queryString += (row[0] + '\n')

        # close cursor object
        cursor.close()

        # if the result from the query is empty, return an error message
        if len(rows) == 0:
            return "No Results Found"
        # otherwise, return the result from the query
        else:
            return queryString

    # if an error occurs trying to open the database, display an error message
    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)
        print('Please select the "Load Data" option to load data into the database, so you can complete your query.')

def loadCSVtoDB():
    try:
        # Start DB connection
        connection = sqlite3.connect('SpotifyData.db')
        # create cursor object
        cursor = connection.cursor()

        # determine if data tables have already been created
        databaseExists = False
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='songs' ''')

        # if there is a table, then the data has already been loaded
        if cursor.fetchone()[0] == 1:
            databaseExists = True

        # Prep the database by cleaning it
        cursor.executescript("""DROP TABLE IF EXISTS "songs";
                                DROP TABLE IF EXISTS "artists";
                                CREATE TABLE "artists" (pmk INTEGER PRIMARY KEY,
                                                                artist VARCHAR(32),
                                                                birthdate VARCHAR(16),
                                                                hometown VARCHAR(64),
                                                                FOREIGN KEY(artist) REFERENCES songs(artist));
                                CREATE TABLE "songs" (pmk INTEGER PRIMARY KEY,
                                                                song VARCHAR(64),
                                                                artist VARCHAR(32),
                                                                genre VARCHAR(32),
                                                                FOREIGN KEY(artist) REFERENCES artists(artist));""")

        # Load the data from 1st CSV into array
        with open('table-1.csv', 'r') as csvFile1:
            reader = csv.DictReader(csvFile1)
            dbArray1 = [(cell['pmk'].strip(), cell['song'].strip(), cell['artist'].strip(), cell['genre'].strip()) for cell in reader]

        # Load the data from 2nd CSV into array
        with open('table-2.csv', 'r') as csvFile2:
            reader = csv.DictReader(csvFile2)
            dbArray2 = [(cell['pmk'].rstrip(), cell['artist'].rstrip(), cell['birthdate'].rstrip(), cell['hometown'].rstrip()) for cell in reader]

        # Dump arrays into database
        cursor.executemany("INSERT INTO songs (pmk, song, artist, genre) VALUES (?, ?, ?, ?);", dbArray1)
        cursor.executemany("INSERT INTO artists (pmk, artist, birthdate, hometown) VALUES (?, ?, ?, ?);", dbArray2)

        # commit databases
        connection.commit()

        # display message for whether the data has already been loaded or not
        if not databaseExists:
            # display message indicating that the data was loaded into the database
            print('The data has been loaded into the database. You can now enter your query')
        else:
            # data has already been loaded
            print('Data has already been loaded into the database')

        # Close DB connection
        connection.close()

    # if error occurs, print error message
    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)

def interpretCommand(userCommand):
    # Extract whatever the first word is of the command, split @ first space
    # Use switch statement to choose which command, or SQL stuff?

    # 1. Split commands into three separate strings @each space - string1 = requested field,
    # string2 = provided field, string3 = field info
    userCommandsList = userCommand.split(", ")

    try:
        # This is the item-type we are requesting
        unknownField = userCommandsList[0]
        knownField = userCommandsList[1]
        knownFieldValue = userCommandsList[2]
    except:
        return ("Error: Commands must be in format [Requested Info], [Known Info], [Known Info Details], " \
               "\n(Type 'help' for an example).")

    # 1.5 Turn all those fields into lowercase
    unknownField = unknownField.lower()
    knownField = knownField.lower()
    knownFieldValue = knownFieldValue.lower()

    # 2. Pass params to database to retrieve and return it.
    return querySQL(unknownField, knownField, knownFieldValue)

def helpMenu():
    print("Welcome to our help menu!")
    print("This system is straight forward, but follows a specific format")
    print("")
    print("To create the database, enter load data")
    print("To end the program, enter exit")
    print("")
    print("Our Categories are | Artist | Genre | Song | Hometown | Birthdate")
    print("")
    print("To get information from our database:")
    print("- Please separate by commas. There must be only one space after each comma")
    print("- DO NOT put information in quotes")
    print("- FIRST value is the information you want to retrieve")
    print("- SECOND value is the Category of information that you know")
    print("- THIRD value is the specific information of the provided category (EX: the artist's real name)")
    print("-------------------------------------------------------------------------------------------")
    print("Here is a working example: ")
    print("Song, Artist, Ed Sheeran")
    print("")
    print("If you are looking for an artist's hometown, here is another example:")
    print("")
    print("Artist, Hometown, London (UK)")

def main():
    # Intro Text
    print("Type 'help' for a list of commands.")

    running = True
    while (running):

        # Get User Input
        menuSelection = input("> ")

        # determine what command the user has entered
        if menuSelection.lower() == "exit":
            running = False
        elif menuSelection.lower() == "load data":
            loadCSVtoDB()
        elif menuSelection.lower() == "help":
            helpMenu()
        else:
            print(interpretCommand(menuSelection))

main()