# Name: Database.py
# Description: Database class implementation
#Author: Hugo
from Table import Table
import os
import shutil
import re
class Database:
    #Constructor.
    def __init__(self, args, isFile):
        self.extension = ".hdb"
        self.tables = []
        self.tableNames = []

        #If database is being built from a directory.
        if isFile:
            self.name = args[0].replace(self.extension, "")
            self.location = args[1] + "//" + args[0]
            allTables = os.listdir(self.location)
            for table in allTables:
                self.tables.append(Table([table, self.location], True))
                self.tableNames.append(self.tables[-1].name)

        #User called for database.
        else:
            self.name = args[0].split(";")[0]
            self.location = self.CreateDatabase(args[1] + "//")
            
    #Makes the actual database directory.
    def CreateDatabase(self, databaseInventory):
        os.mkdir(databaseInventory + self.name + self.extension)
        return databaseInventory + self.name + self.extension

    #Opens all table directories to make tables.
    def OpenTables(self):
        for dir, subdirs, file in os.walk(self.location):
            for table in subdirs:
                self.tables.append(Table([table, dir], True))
        for table in self.tables:
            self.tablesNames.append(table.name)
    
    #Ensures user calling create table will not cause issues
    def CreateTable(self, userArgs):
        if userArgs.split()[1].replace(";","") in self.tableNames:
                print("!Failed to create database {dbName} because it already exists.".format(dbName = userArgs.split()[1].replace(";","")))
        else:
            self.tables.append(Table([userArgs, self.location], False))
            self.tableNames.append(self.tables[-1].name)

    #Ensures user calling drop table will not cause issues and deletes the table.
    def DropTable(self, userArgs):
        if userArgs in self.tableNames:
            tableIndex = self.tableNames.index(userArgs)
            tableTrash = self.tables.pop(tableIndex)
            shutil.rmtree(tableTrash.location, True)
            self.tableNames.pop(tableIndex)
            print("Table {tbName} deleted.".format(tbName = userArgs))
        else:
            print("!Failed to delete {tbName} because it does not exist.".format(tbName = userArgs))
    
    #Selects data from tables in database based on user input.
    def SelectTable(self, userArgs):
        if len(userArgs.split(" from ")) != 0:
            columnAndTable = userArgs.split(" from ")
            selectedTables = columnAndTable[1].split(", ")
            displayString = ""
            for table in selectedTables:
                if table.replace('\n', "") in self.tableNames:
                    tableIndex = self.tableNames.index(table.replace('\n', ""))
                    displayString += self.displayTable(self.tables[tableIndex])
                else:
                    columnAndTable[0] = "*"
                    displayString = "!Failed to query table {missing} because it does not exist.".format(missing = table).replace("\n","")
            if columnAndTable[0] == "*":
                print(displayString)

    #Alters table based on user input.
    def AlterTable(self, userArgs):
        if len(userArgs.split()) >= 4:
            if userArgs.split()[1] in self.tableNames:
                tableIndex = self.tableNames.index(userArgs.split()[1])
                if "add" in userArgs:
                    tableHolder = self.tables[tableIndex]
                    file = open(tableHolder.location + "//" + tableHolder.templateName, "r")
                    currentList = file.read()
                    file.close()
                    newItems = userArgs.split(" add ")[1].replace("\n","")
                    for pair in newItems.split(", "):
                        tableHolder.IdentifyTypes(pair.split()[1])
                        tableHolder.attributes.append(pair.split()[0])
                        currentList += " | {tbAttr} {tbType}".format(tbType = tableHolder.types[-1], tbAttr = tableHolder.attributes[-1])
                    file = open(tableHolder.location + "//" + tableHolder.templateName, "w")
                    file.write(currentList)
                    file.close()
                print("Table {tbName} modified.".format(tbName = self.tableNames[tableIndex]))
            else:
               print("!Failed to alter table {dbName} because it does not exist.".format(dbName = userArgs.split()[1].replace(";","")))
        else:
            print("!Syntax Error. There are too few arguments.")

    #Reads table info from a file.
    def displayTable(self, table):
        file = open(table.location  + "//" + table.templateName, "r")
        returnString = file.read()
        file.close()
        return returnString