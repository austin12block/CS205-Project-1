import sqlite3
#SQL Instructions:

def main():
    #test
    userCommand = input("Enter a command: ")

    interpretCommand(userCommand)

def interpretCommand(userCommand):

    #Pseudocode:
    #Extract whatever the first word is of the command, split @ first space
    #Use switch statement to choose which command, or SQL stuff?

main()