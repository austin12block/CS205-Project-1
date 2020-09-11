import sqlite3, csv
from sqlite3 import Error

#SQL Instructions:
def querieSQL():
    try:
        # connect to the database
        connectSQLite = sqlite3.connect('topSpotifySongs.db')

        # create cursor object which will be used for queries
        cursor = connectSQLite.cursor()
        print('Connected to SQLite')

        cursor.execute("SELECT * FROM TopSpotifySongs WHERE artist = 'Ed Sheeran'")
        rows = cursor.fetchall()

        for row in rows:
            for cell in row:
                print(str(cell))

        #connectSQLite.commit()

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
                                CREATE TABLE "TopSpotifySongs" (pmk INTEGER PRIMARY KEY,
                                                                song VARCHAR(64),
                                                                artist VARCHAR(32),
                                                                genre VARCHAR(32));
                                CREATE TABLE "TopArtistData" (pmk INTEGER PRIMARY KEY,
                                                                artist VARCHAR(32),
                                                                birthdate VARCHAR(16),
                                                                hometown VARCHAR(64));""")
        # Load the data from 1st CSV into array
        with open('table-1.csv', 'r') as csvFile1:
            reader = csv.DictReader(csvFile1)
            dbArray1 = [(cell['pmk'].rstrip(), cell['song'].rstrip(), cell['artist'].rstrip(), cell['genre'].rstrip()) for cell in reader]
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
    #2. Check if command words are valid - see if column titles are in an array of valid options
    #3. Based on each command, pass to database to retrieve.
    #4. Take output result from database and return it.
    #5. Print out that result.

    #string -> request, provided, providedInfo
    unknownField, knownField, knownFieldValue
    if knownField == song:
        unknownFieldValue = doSongQuery(unknownField, knownFieldValue) #Pass request string and field info
        print(unknownFieldValue)



def main():
    # establish SQLite connection
    # createSQLConnection()

    loadCSVtoDB()
    querieSQL()

    #test
    userCommand = input("Enter a command: ")

    interpretCommand(userCommand)


main()