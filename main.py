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
                                CREATE TABLE "TopSpotifySongs" (pmk INTEGER PRIMARY KEY,
                                                                song VARCHAR(64),
                                                                artist VARCHAR(32),
                                                                genre VARCHAR(32));
                                CREATE TABLE "TopArtistData" (pmk INTEGER PRIMARY KEY,
                                                                artist VARCHAR(32),
                                                                birthdate VARCHAR(16),
                                                                hometown VARCHAR(64));""")
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


def main():
    # establish SQLite connection
    # createSQLConnection()

    loadCSVtoDB()
    querySQL('song', 'TopSpotifySongs', 'artist', 'Ed Sheeran')

    #test
    userCommand = input("Enter a command: ")

    interpretCommand(userCommand)

def interpretCommand(userCommand):
    pass
    #Pseudocode:
    #Extract whatever the first word is of the command, split @ first space
    #Use switch statement to choose which command, or SQL stuff?

main()