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
            ColumnsTableAndFilters = userArgs.split(" from ")
            tableAndFilters = ColumnsTableAndFilters[1].split(" where ", 1)
            selectedTables = tableAndFilters[0].split(", ")
            displayString = ""
            for table in selectedTables:
                if table.replace('\n', "") in self.tableNames:
                    tableIndex = self.tableNames.index(table.replace('\n', ""))
                    if ColumnsTableAndFilters[0] == "*":
                        displayString += self.displayTable(self.tables[tableIndex], self.tables[tableIndex].attributes, tableAndFilters)
                    else:
                        columns = ColumnsTableAndFilters[0].split(", ")
                        displayString += self.displayTable(self.tables[tableIndex], columns, tableAndFilters)

                else:
                    displayString = "!Failed to query table {missing} because it does not exist.".format(missing = table).replace("\n","")
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

    #inserts user values into table
    def InsertValues(self, userArgs):
        if userArgs.split()[0] == "into":
            if userArgs.split()[1] in self.tableNames:
                tableIndex = self.tableNames.index(userArgs.split()[1])
                if userArgs.split()[2].split("(")[0] == "values":
                    combinedValues = userArgs.split("values")[1].replace(")","").replace("(","")
                    splitValues = combinedValues.split(", ")
                    self.tables[tableIndex].InsertValues(splitValues)
                    print("1 new record inserted.")
                else:
                 print("!Syntax Error. The command is INSERT INTO tableName VALUES (values)")   
            else:
                print("!That table does not exist in this database.")
        else:
            print("!Syntax Error. The command is INSERT INTO tableName VALUES (values)")
    
    #Deletes values from table
    def DeleteValues(self, userArgs):
        tableAndCond = userArgs.replace("from ","").split(" where ")
        if len(tableAndCond) == 2:
            if tableAndCond[0] in self.tableNames:
                tableIndex = self.tableNames.index(tableAndCond[0])
                selectedTable = self.tables[tableIndex]
                fufilledValues = self.tables[tableIndex].Where(tableAndCond[1].split())
                valueFileName = []
                for fufilledValue in fufilledValues:
                    fileName = ""
                    for values in fufilledValue:
                        fileName += values
                    selectedTable.items.remove(fufilledValue)
                    os.remove(selectedTable.location + "//" + fileName + selectedTable.itemExtension)
                print("{amountRemoved} records deleted.".format(amountRemoved = len(fufilledValues)))

    def UpdateValues(self, userArgs):
        print("Update")

        


    #display table
    def displayTable(self, table, columns, hasWhere):
        returnString = ""
        attributeIndexes = []
        displayValues = []
        if len(hasWhere) == 1:
            displayValues = table.items
        else:
            displayValues = table.Where(hasWhere[1].split())
        #Gets index of each attribute desired.
        for currAttribute in table.attributes:
            if currAttribute in columns:
                attributeIndexes.append(table.attributes.index(currAttribute))
        
        #Gets attribute name and type of table.
        for attributeIndex in attributeIndexes:
            if attributeIndex == attributeIndexes[-1]:
                returnString += "{attrName} {attrType}\n".format(attrName = table.attributes[attributeIndex], attrType = str(table.types[attributeIndex]))
            else:
                returnString += "{attrName} {attrType} | ".format(attrName = table.attributes[attributeIndex], attrType = str(table.types[attributeIndex]))

        #Gets attributes of each item.
        for tableItem in displayValues:
            for attributeIndex in attributeIndexes:
                if attributeIndex == attributeIndexes[-1]:
                    returnString += "{displayItem}\n".format(displayItem = tableItem[attributeIndex])
                else:
                    returnString += "{displayItem} | ".format(displayItem = tableItem[attributeIndex])
        return returnString
                

