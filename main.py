import sqlite3, csv
from sqlite3 import Error

#SQL Instructions:
def querySQL(unknownField, tableName, knownField, knownFieldValue):
    try:
        # connect to the database
        connectSQLite = sqlite3.connect('topSpotifySongs.db')

        # create cursor object which will be used for queries
        cursor = connectSQLite.cursor()

        # create query
        query = "SELECT " + unknownField + " FROM " + tableName + " WHERE " + knownField + " = '" + knownFieldValue + "'"

        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row[0])

        # close cursor object
        cursor.close()

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)

def loadCSVtoDB():
    try:
        # Start DB connection
        connection = sqlite3.connect('topSpotifySongs.db')
        cursor = connection.cursor()
        # Prep the database by cleaning it

        cursor.executescript("""DROP TABLE IF EXISTS "TopSpotifySongs";
                                DROP TABLE IF EXISTS "TopArtistData";
                                CREATE TABLE "TopArtistData" (pmk INTEGER PRIMARY KEY,
                                                                artist VARCHAR(32),
                                                                birthdate VARCHAR(16),
                                                                hometown VARCHAR(64));
                                CREATE TABLE "TopSpotifySongs" (pmk INTEGER PRIMARY KEY,
                                                                song VARCHAR(64),
                                                                artist VARCHAR(32),
                                                                genre VARCHAR(32),
                                                                FOREIGN KEY (artist) REFERENCES TopArtistData (artist));""")
        # TODO: foreign key
        # FOREIGN KEY (artist) REFERENCES TopArtistData (artist)
        # Load the data from 1st CSV into array
        with open('table-1.csv', 'r') as csvFile1:
            reader = csv.DictReader(csvFile1)
            dbArray1 = [(cell['pmk'].strip(), cell['song'].strip(), cell['artist'].strip(), cell['genre'].strip()) for cell in reader]
        # Load the data from 1st CSV into array
        with open('table-2.csv', 'r') as csvFile2:
            reader = csv.DictReader(csvFile2)
            dbArray2 = [(cell['pmk'].rstrip(), cell['artist'].rstrip(), cell['birthdate'].rstrip(), cell['hometown'].rstrip()) for cell in reader]
        # Dump arrays into database
        cursor.executemany("INSERT INTO TopSpotifySongs (pmk, song, artist, genre) VALUES (?, ?, ?, ?);", dbArray1)
        cursor.executemany("INSERT INTO TopArtistData (pmk, artist, birthdate, hometown) VALUES (?, ?, ?, ?);", dbArray2)
        connection.commit()
        # Close DB connection
        connection.close()
    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)

def interpretCommand(userCommand):
    #pass
    #Pseudocode:
    #Extract whatever the first word is of the command, split @ first space
    #Use switch statement to choose which command, or SQL stuff?


    #TODO: Add thing to ignore case
    #TODO: Split off at first space

    #1. Split commands into three separate strings @each space - string1 = requested field, string2 = provided field, string3 = field info
    commandList = userCommand.split(", ")

    unknownField = commandList[0] #This is the item-type we are requesting
    knownField = commandList[1]
    knownFieldValue = commandList[2]

    print(commandList)

    #1.5 Turn all those field into lowercase
    unknownField = unknownField.lower()
    knownField = knownField.lower()
    knownFieldValue = knownFieldValue.lower()
    print(unknownField+knownField+knownFieldValue)

    #2. Check if command words are valid - see if column titles are in an array of valid options
    #3. Based on each command, pass to database to retrieve.
    #4. Take output result from database and return it.
    #5. Print out that result.

    #string -> request, provided, providedInfo

    if knownField == "song":
        # Pass request string and field info
        # unknownFieldValue = doSongQuery(unknownField, knownFieldValue)
        # print(unknownFieldValue)
        print("song")
    elif knownField == "artist":
        # unknownFieldValue = doArtistQuery(unknownField, knownFieldValue)
        # print(unknownFieldValue)
        print("artist")
    elif knownField == "genre":
        # unknownFieldValue = doGenreQuery(unknownField, knownFieldValue)
        # print(unknownFieldValue)
        print("genre")
    elif knownField == "birthdate":
        # unknownFieldValue = doBirthdateQuery(unknownField, knownFieldValue)
        # print(unknownFieldValue)
        print("birthdate")
    elif knownField == "hometown":
        # unknownFieldValue = doHometownQuery(unknownField, knownFieldValue)
        # print(unknownFieldValue)
        print("hometown")



def main():
    # establish SQLite connection
    # createSQLConnection()

    loadCSVtoDB()
    querySQL('song', 'TopSpotifySongs', 'artist', 'Ed Sheeran')

    #test
    while (1==1): #temporary inf. loop for testing
        userCommand = input("Enter a command (Use commas to separate items): ")

        interpretCommand(userCommand)


main()