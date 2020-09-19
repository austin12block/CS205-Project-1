import sqlite3, csv
from sqlite3 import Error

# SQL Instructions:
def querySQL(unknownField, knownField, knownFieldValue):
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

        # switch statement for unknownField ti help create query statement
        if unknownField == "artist" or unknownField == "birthdate" or unknownField == "hometown":
            unknownFieldAppended = "artists." + unknownField
        elif unknownField == "song" or unknownField == "genre":
            unknownFieldAppended = "songs." + unknownField
        else:
            return "Could not complete query for " + unknownField + " field"

        # create query
        query = "SELECT DISTINCT " + unknownFieldAppended + " FROM songs INNER JOIN artists ON songs.artist = artists.artist WHERE " + knownFieldAppended + "='" + knownFieldValue + "' COLLATE NOCASE"

        print("QUERY: " + query)

        # execute the query and get the needed information from the database
        cursor.execute(query)
        rows = cursor.fetchall()

        queryString = ''
        # go through each row of returned field to get the unknown values
        for row in rows:
            # print(row[0])
            # create return string from query
            queryString += (row[0] + '\n')

        # close cursor object
        cursor.close()

        # if the result from the query is empty, return an error message
        if len(rows) == 0:
            # print("Could not complete query for " + unknownField + " field")
            return "Could not complete query for " + unknownField + " field"
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

        # display message indicating that the data was loaded into the database
        print("The data has been loaded into the database")

        # Close DB connection
        connection.close()

    # if error occurs, print error message
    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)


def interpretCommand(userCommand):
    #Pseudocode:
    #Extract whatever the first word is of the command, split @ first space
    #Use switch statement to choose which command, or SQL stuff?


    #TODO: Add thing to ignore case
    #TODO: Split off at first space

    # 1. Split commands into three separate strings @each space - string1 = requested field, string2 = provided field, string3 = field info
    userCommandsList = userCommand.split(", ")

    try:
        unknownField = userCommandsList[0] # This is the item-type we are requesting
        knownField = userCommandsList[1]
        knownFieldValue = userCommandsList[2]
    except:
        return "Did not work, did you forget to use commas?"

    print(userCommandsList)

    # 1.5 Turn all those field into lowercase
    unknownField = unknownField.lower()
    knownField = knownField.lower()
    knownFieldValue = knownFieldValue.lower()
    print(unknownField + " " + knownField + " " + knownFieldValue)

    # 2. Check if command words are valid - see if column titles are in an array of valid options
    possibleCommandsList = ["song", "artist", "genre", "birthdate", "hometown"]
    if unknownField in possibleCommandsList and knownField in possibleCommandsList:
        # 3. Pass params to database to retrieve and return it.
        return querySQL(unknownField, knownField, knownFieldValue)
    else:
        # 3.5 otherwise invalid input
        return "Invalid input"

    # string -> request, provided, providedInfo

    # if knownField == "song":
    #     # Pass request string and field info
    #     # unknownFieldValue = doSongQuery(unknownField, knownFieldValue)
    #     # print(unknownFieldValue)
    #     print("song")
    # elif knownField == "artist":
    #     # unknownFieldValue = doArtistQuery(unknownField, knownFieldValue)
    #     # print(unknownFieldValue)
    #     print("artist")
    # elif knownField == "genre":
    #     # unknownFieldValue = doGenreQuery(unknownField, knownFieldValue)
    #     # print(unknownFieldValue)
    #     print("genre")
    # elif knownField == "birthdate":
    #     # unknownFieldValue = doBirthdateQuery(unknownField, knownFieldValue)
    #     # print(unknownFieldValue)
    #     print("birthdate")
    # elif knownField == "hometown":
    #     # unknownFieldValue = doHometownQuery(unknownField, knownFieldValue)
    #     # print(unknownFieldValue)
    #     print("hometown")


def main():
    # establish SQLite connection
    # createSQLConnection()

    # loadCSVtoDB()
    # # What you want, what you know, what it is
    # # test cases --- delete later
    # querySQL('artist', 'hometown', 'saNta Barbara (CA)')
    # print("-----------")
    # querySQL('genre', 'hometown', 'sanTa Barbara (CA)')
    # print("-----------")
    # querySQL('song', 'hometown', 'santA Barbara (CA)')
    # print("-----------")
    # querySQL('birthdate', 'hometown', 'santa Barbara (CA)')
    # print("-----------")
    # querySQL('artist', 'genre', 'POP')
    # print("-----------")
    # querySQL('artist', 'song', 'senorita')
    # print("-----------")
    # querySQL('genre', 'birthdate', '4-juL-95')
    # print("-----------")
    # querySQL('genre', 'song', 'vermOnt')
    # end of test cases

    running = True
    while (running):

        # Get User Input
        menuSelection = input("(1) Search Query\n(2) Exit\n(3) Load Data\n")

        # Input Validation
        # while menuSelection != "1" and menuSelection != "2" and menuSelection != "3":
        while menuSelection != "1" and menuSelection.lower() != "exit" and menuSelection.lower() != "load data":
            menuSelection = input("(1) Search Query\n(2) Exit\n(3) Load Data\n")

        # 1. Search Query
        if menuSelection == "1":
            # EXAMPLE TEST INPUT: "Artist, Song, China" <- without quotes
            userCommand = input("Enter a command (Use commas to separate items): ")

            # Print return value
            print(interpretCommand(userCommand))

        # 2. Exit
        # elif menuSelection == "2":
        elif menuSelection.lower() == "exit":
            running = False

        # Load Data
        elif menuSelection.lower() == "load data":
            loadCSVtoDB()


main()