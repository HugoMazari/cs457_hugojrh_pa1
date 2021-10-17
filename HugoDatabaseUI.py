# Name: HugoDatabaseUI.py
# Description: Main program for Hugo's Database
#Author: Hugo 

from Database import Database
import Types
import os
import shutil
import sys
import re
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
        allDatabases = os.listdir(DatabaseStorage)
        for database in allDatabases:
                Databases.append(Database([database, DatabaseStorage], True))
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
                print("Database {dbName} created.".format(dbName = userArgs.split()[1].replace(";","")))
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
                    print("Table {dbName} created.".format(dbName = userArgs.split()[1].replace(";","")))
            else:
                print("!Syntax Error. There are too few arguments.")
        else:
            print("!No database selected.")
    else:
        print("!Failed to create {itemName} because it is not a supported item.".format(itemName = userArgs.split()[0]))

#Drops either a database or a table.
def Drop(userArgs):
    if userArgs.split()[0] == "database":
        if userArgs.split()[1].replace(";","") in DatabaseNames:
            databaseIndex = DatabaseNames.index(userArgs.split()[1].replace(";",""))
            databaseTrash = Databases.pop(databaseIndex)
            shutil.rmtree(databaseTrash.location, True)
            DatabaseNames.pop(databaseIndex)
            print("Database {dbName} deleted.".format(dbName = userArgs.split()[1].replace(";","")))
        else:
            print("!Failed to delete {dbName} because it does not exist.".format(dbName = userArgs.split()[1].replace(";","")))
    elif userArgs.split()[0] == "table":
        if CurrentDatabase != None:
            Databases[CurrentDatabase].DropTable(userArgs.split()[1].replace(";",""))
        else:
            print("!No database selected.")
    else:
        print("!Failed to delete {itemName} because it is not a supported item.".format(itemName = userArgs.split()[0]))

#Chooses database to focus on.
def Use(userArgs):
    global CurrentDatabase
    if userArgs.split()[0].replace(";","") in DatabaseNames:
        CurrentDatabase = DatabaseNames.index(userArgs.split()[0].replace(";",""))
        print("Using database {dbName}.".format(dbName = userArgs.split()[0].replace(";","")))
    else:
        print("Cannot use {dbName} because it does not exist.".format(dbName = userArgs.split()[0].replace(";","")))

#Selects attributes from table to display
def Select(userArgs):
    if CurrentDatabase != None:
        Databases[CurrentDatabase].SelectTable(userArgs.replace(";",""))
    else:
        print("!No database selected.")

#Alters table attributes
def Alter(userArgs):
    if CurrentDatabase != None:
        Databases[CurrentDatabase].AlterTable(userArgs.replace(";",""))
    else:
        print("!No database selected.")

def Insert(userArgs):
    if CurrentDatabase != None:
        Databases[CurrentDatabase].InsertValues(userArgs.replace(";",""))
    else:
        print("!No database selected.")


#Determines user's choice.
def SqlChoices(commandAndArgs):
    userCommand = commandAndArgs.split(" ", 1)[0]
    if userCommand == "quit;":
        print("All done.")
        sys.exit()
    else:
        if len(commandAndArgs.split(" ", 1)) == 2:
            userArgs = commandAndArgs.split(" ", 1)[1]
            if userCommand == "create":
                Create(userArgs)
            elif userCommand == "drop":
                Drop(userArgs)
            elif userCommand == "use":
                Use(userArgs)
            elif userCommand == "select": 
                Select(userArgs)
            elif userCommand == "alter":
                Alter(userArgs)
            else:
                print("!Unknown command.")
        else:
            print("!Invalid syntax. All commands must have at least one argument.")


#Function to take in user input. WIP
def UserInput(firstTime = False):
    userInput = GetUserInput(firstTime).lower()
    userCommand = userInput.split(" ", 1)[0]
    SqlChoices(userInput)
    UserInput()


#Gets user input.
def GetUserInput(firstTime):
    if firstTime:
        print("To exit type \"quit;\". Query must end with a semicolon.")
    userInput = input("Hugo's Database> ")
    while userInput[-1] != ';':
        userInput += input("            ...> ")
    return userInput

#Function to read file commands.
def ReadFile():
    #Gets file name
    print("Please type the path of your choice of file.")
    userInput = input("Hugo's Database> ")
    while os.path.exists(userInput) != True:
        userInput = input("This file is unusable. Please try again.\n            ...> ")
    #Opens file and reads first line
    file = open(userInput, 'r')
    fileCommand = file.readline().replace("\n", "")
    #While file is not wanting to exit
    while fileCommand.lower() != ".exit\n":
        if re.search("^--", fileCommand.lower()) == None and fileCommand.lower() != "\n":
            SqlChoices(KeywordDetection(fileCommand))
        fileCommand = file.readline()
    print("All done.")

def KeywordDetection(userInput):
    returnValue = ""
    for word in userInput.split():
        if word.lower() in Types.Keywords.Keyword:
            returnValue += word.lower()
        else:
            returnValue += word
        if word != userInput.split()[-1]:
            returnValue += " "
    return returnValue



main()