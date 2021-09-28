from Database import Database
import os
import shutil
#Global variables
DatabaseStorage = "Hugo-s_Database_Directory"
CurrentDatabase = None
Databases = []
DatabaseNames = []

# Program entry point.
def main():
    # Makes necessary directory to store databases.
    LoadDatabaseInventory()

    #Determines user's method of input, a file or typing.
    inputChoice = input("You can use q to quit.\nPlease select your choice of input of (f)ile or (t)yping: ").lower()[0]
    if inputChoice == "f":
        ReadFile()
    elif inputChoice == "t":
        UserInput(True)
    elif inputChoice == "q":
        print("\nGoodbye!\n")
    else:
        print("\nThat is not a valid choice. Please try again.\n")
        main()

#Loads previous databases and tables.
def LoadDatabaseInventory():
    ifFile = os.path.isdir(DatabaseStorage)
    if ifFile != True:
        os.mkdir(DatabaseStorage)
    else:
        for dir, subdirs, file in os.walk(DatabaseStorage):
            for database in subdirs:
                Databases.append(Database([database, dir], True))
        for database in Databases:
            DatabaseNames.append(database.name)

#Creates either a database or table.
def Create(userArgs):
    #Database Creation
    if userArgs.split()[0] == "database":
        if len(userArgs.split()) == 2:
            if userArgs.split()[1].replace(";","") in DatabaseNames:
                print("!Failed to create database {dbName} because it already exists.".format(dbName = userArgs.split()[1].replace(";","")))
            else:
                Databases.append(Database([userArgs.split(" ", 1)[1], DatabaseStorage], False))
                DatabaseNames.append(Databases[-1].name)
        else:
            print("!Syntax Error. There are too many or too few arguments.")
    #Table creation
    elif userArgs.split()[0] == "table":
        if CurrentDatabase != None:
            if len(userArgs.split()) >= 4:
                if userArgs.split()[1] in Databases[CurrentDatabase].tableNames:
                    print("!Failed to create table {dbName} because it already exists.".format(dbName = userArgs.split()[1].replace(";","")))
                else:
                    Databases[CurrentDatabase].CreateTable(userArgs)
            else:
                print("!Syntax Error. There are too few arguments.")
        else:
            print("!No database selected.")
    else:
        print("!Failed to creal {itemName} because it is not a supported item.".format(itemName = userArgs.split()[0]))

#Drops either a database or a table.
def Drop(userArgs):
    if userArgs.split()[0] == "database":
        if userArgs.split()[1].replace(";","") in DatabaseNames:
            databaseIndex = DatabaseNames.index(userArgs.split()[1].replace(";",""))
            databaseTrash = Databases.pop(databaseIndex)
            shutil.rmtree(databaseTrash.location, True)
            DatabaseNames.pop(databaseIndex)

        else:
            print("!Failed to delete {dbName} because it does not exist.".format(dbName = userArgs.split()[1].replace(";","")))

#Chooses database to focus on.
def Use(userArgs):
    global CurrentDatabase
    if userArgs.split()[0].replace(";","") in DatabaseNames:
        CurrentDatabase = DatabaseNames.index(userArgs.split()[0].replace(";",""))
        print("Using database {dbName}.".format(dbName = userArgs.split()[0].replace(";","")))
    else:
        print("!Database {dbName} does not exist.".format(dbName = userArgs.split()[0].replace(";","")))      


#Function to take in user input. WIP
def UserInput(firstTime = False):
    userInput = GetUserInput(firstTime).lower()
    userCommand = userInput.split(" ", 1)[0]
    if userCommand == "quit;":
        print("\nGoodbye!\n")
    else:
        userArgs = userInput.split(" ", 1)[1]
        if userCommand == "create":
            Create(userArgs)
        elif userCommand == "drop":
            Drop(userArgs)
        elif userCommand == "use":
            Use(userArgs)
        UserInput()


#Gets user input.
def GetUserInput(firstTime):
    if firstTime:
        print("To exit type \"quit;\". Query must end with a semicolon.")
    userInput = input("Hugo'sDatabase> ")
    while userInput[-1] != ';':
        userInput += input("           ...> ")
    return userInput

#Function to read file commands. WIP
def ReadFile():
    print("Now taking file name")


main()