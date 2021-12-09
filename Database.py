# Name: Database.py
# Description: Database class implementation
#Author: Hugo
from typing import List
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
    
    #Checks if there is a transaction in progress aside from the one calling the function.
    def CheckForForeignTransaction(self, name, transLock, mainDBLocation):
        hasForeignLock = False
        if name in self.tableNames:
            tableIndex = self.tableNames.index(name)
            tableDir = self.tables[tableIndex].location
            tableDir = re.sub("^\S*\//" + self.name, mainDBLocation + "//" + self.name, tableDir)
            for file in os.listdir(tableDir):
                if file.endswith(".lk"):
                    if transLock == None:
                        hasForeignLock = True
                        break
                    elif file.find(transLock) == -1:
                        hasForeignLock = True
                        break

    def CreateLock(self, name, transLock, mainDBLocation):
        if name in self.tableNames:
            tableIndex = self.tableNames.index(name)
            tableDir = self.tables[tableIndex].location
            transLockFile = tableDir + "//" + transLock +".lk"
            transLockFile = re.sub("^\S*\//" + self.name, mainDBLocation + "//" + self.name, transLockFile)
            open(transLockFile, "x")

    #Ensures user calling create table will not cause issues
    def CreateTable(self, userArgs):
        if userArgs.split()[1].split("(")[0] in self.tableNames:
                print("!Failed to create database {dbName} because it already exists.".format(dbName = userArgs.split()[1].split("(")[0]))
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
            #Variable declaration
            ColumnsTableAndFilters = userArgs.split(" from ") #Splits columns to display from tables and conditions
            joinType = self.DiscoverJoinType(ColumnsTableAndFilters[1]) #Determines the type of join
            tableAndFilters = "" 
            if joinType == ", ": #Splits tables to select from conditions
                tableAndFilters = ColumnsTableAndFilters[1].split(" where ", 1) 
            else:
                tableAndFilters = ColumnsTableAndFilters[1].split(" on ", 1)
            selectedTables = tableAndFilters[0].split(joinType) #Splits tables based on join type
            displayString = ""
            tableIndex = []
            columns = []

            #Checks if table is given a separate name
            for table in selectedTables:
                if " " in table:
                    selectedTables[selectedTables.index(table)] = table.split()
            
            #Checks if tables queued exist
            for table in selectedTables:
                tableName = table
                if type(table) is list:
                    tableName = table[0]
                if tableName.replace('\n', "") in self.tableNames:
                    tableIndex.append(self.tableNames.index(tableName.replace('\n', "")))
                else:
                    displayString = "!Failed to query table {missing} because it does not exist.\n".format(missing = table).replace("\n","")

            
            if ColumnsTableAndFilters[0] == "*":
                for index in tableIndex:
                    columns.append(self.tables[index].attributes)
            else:
                columns.append(ColumnsTableAndFilters[0].split(", "))
            displayString = self.displayTable(joinType, tableIndex, columns, tableAndFilters)

            print(displayString)

    #Alters table based on user input.
    def AlterTable(self, userArgs, transLock, transLockLocation):
        if len(userArgs.split()) >= 4:            
            if userArgs.split()[1] in self.tableNames:
                if self.CheckForForeignTransaction(userArgs.split()[1], transLock, transLockLocation) == False:
                    if transLock != None:
                        self.CreateLock(userArgs.split()[1], transLock, transLockLocation)
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
                    print("Error: Table {tblName} is locked!".format(tblName = userArgs.split()[1]))
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
                for fufilledValue in fufilledValues:
                    fileName = ""
                    for values in fufilledValue:
                        fileName += values
                    selectedTable.items.remove(fufilledValue)
                    os.remove(selectedTable.location + "//" + fileName + selectedTable.itemExtension)
                print("{amountRemoved} records deleted.".format(amountRemoved = len(fufilledValues)))

    def UpdateValues(self, userArgs, transLock, mainDBLocation):
        if userArgs.find("set") != -1 and userArgs.find("where") != -1:
            tableName = userArgs.split()[0]
            if tableName in self.tableNames:
                if self.CheckForForeignTransaction(tableName, transLock, mainDBLocation) == False:
                    if transLock != None:
                        self.CreateLock(tableName, transLock, mainDBLocation)
                    tableIndex = self.tableNames.index(tableName)
                    selectedTable = self.tables[tableIndex]
                    tableFilters = userArgs.split(" where ")[1].split()
                    selectedValues = selectedTable.Where(tableFilters)
                    targetedAttrAndNewValue = userArgs.replace("set","where").split(" where ")[1].split()
                    targetedAttr = targetedAttrAndNewValue[0]
                    newValue = targetedAttrAndNewValue[2].replace("\'","")
                    selectedTable.ModifyValues(selectedValues, targetedAttr, newValue)
                    print("{amount} record{s} modified.".format(amount = len(selectedValues), \
                        s = "s" if len(selectedValues) > 1 else ""))
                else:
                    print("Error: Table {tblName} is locked!".format(tblName = tableName))


    #display table
    def displayTable(self, joinType, tableIndex, columns, hasWhere):
        #Variables                if tableIndexAndNumbers(
        returnString = "" #Strings to Return
        attributeIndexes = []
        displayValues = []
        whereRequirements = []
        tableNickNames = []
        #Checks if filters exist
        if len(hasWhere) == 1:
            if joinType == ", " or joinType == "default":
                for index in tableIndex:
                    displayValues.append(self.tables[index].items)
            else:
                return "!Syntax Error. All joins must have at least one ON."
        else:
            tableAndNicknames = hasWhere[0].split(joinType)
            for table in tableAndNicknames:
                tableNickNames.append(table.split(" ")[1])
            whereRequirements = hasWhere[1].split()

            if joinType == ", " or joinType == " inner join ":
                whereArgs = self.FormatVariablesForWhere(whereRequirements, [tableIndex, tableNickNames])
                displayValues.append(self.tables[tableIndex[0]].Where(whereArgs))
                whereRequirements.reverse()
                whereArgs = self.FormatVariablesForWhere(whereRequirements,[tableIndex, tableNickNames])
                displayValues.append(self.tables[tableIndex[1]].Where(whereArgs))
                #still rendered uneven. Make function to compare the two lists, and extend the shorter one to match.

            elif joinType == " left outer join ":
                displayValues.append(self.tables[tableIndex[0]].items)
                whereRequirements.reverse()
                whereArgs = self.FormatVariablesForWhere(whereRequirements,[tableIndex, tableNickNames])
                displayValues.append(self.tables[tableIndex[1]].Where(whereArgs))

            #Single table
            else:
                whereArgs = self.FormatVariablesForWhere(whereRequirements, [tableIndex, tableNickNames])
                displayValues.append(self.tables[tableIndex[0]].Where(whereArgs))

        if len(displayValues) != 1:
            #Extend shorter list
            displayValues = self.MatchItems(joinType, displayValues, [tableIndex, tableNickNames], whereRequirements)

        #Gets index of each attribute desired.
        for index in tableIndex:
            tableCurrAttr = []
            for currAttribute in self.tables[index].attributes:
                if currAttribute in columns[index]:
                    tableCurrAttr.append(self.tables[index].attributes.index(currAttribute))
            attributeIndexes.append(tableCurrAttr)
        
        #Gets attribute name and type of table.
        for tableAttrIndex in tableIndex:
            for attributeIndex in attributeIndexes[tableAttrIndex]:
                if tableAttrIndex == tableIndex[-1] and attributeIndex == attributeIndexes[tableAttrIndex][-1]:
                    returnString += "{attrName} {attrType}\n".format(attrName = self.tables[tableAttrIndex].attributes[attributeIndex], attrType = str(self.tables[tableAttrIndex].types[attributeIndex]))
                else:
                    returnString += "{attrName} {attrType} | ".format(attrName = self.tables[tableAttrIndex].attributes[attributeIndex], attrType = str(self.tables[tableAttrIndex].types[attributeIndex]))

        #Gets attributes of each item.
        for x in range(0, len(displayValues[0])):
            for tableAttrIndex in range(0, len(displayValues)):
                for attributeIndex in attributeIndexes[tableAttrIndex]:
                    if displayValues[tableAttrIndex] == displayValues[-1] and attributeIndex == attributeIndexes[tableAttrIndex][-1]:
                        returnString += "{displayItem}\n".format(displayItem = displayValues[tableAttrIndex][x][attributeIndex])
                    else:
                        returnString += "{displayItem} | ".format(displayItem = displayValues[tableAttrIndex][x][attributeIndex])
        return returnString

    #Determines what kind of join it is.
    def DiscoverJoinType(self, tablesSelected):
        joinType = None
        if ", " in tablesSelected:
            joinType = ", "
        elif "inner" in tablesSelected:
            joinType = " inner join "
        elif "left outer" in tablesSelected:
            joinType = " left outer join "
        elif "right outer" in tablesSelected:
            joinType = " right outer join "
        else:
            joinType = "default"
        return joinType

    def FormatVariablesForWhere(self, userArgs, tableIndexAndNumbers = None):
        """
        Please don't forget the tableIndexAndNumber if tables are defined with names.
        """
        formattedVariables = []
        tableNameRe = re.compile("^[a-zA-Z]*\.")
        if len(userArgs) == 3:
            #The target of the item
            if tableNameRe.match(userArgs[0]) != None:
                tableAndItem = userArgs[0].split(".") #Turns T.Item to [T, Item]
                formattedVariables.append(tableAndItem[1])
            else:
                formattedVariables.append(userArgs[0])

            #Don't mess with comparison variable
            formattedVariables.append(userArgs[1])

            if tableNameRe.match(userArgs[2]) != None:
                tableAndItem = userArgs[2].split(".") #Turns T.Item to [T, Item]
                tableNameIndex = tableIndexAndNumbers[1].index(tableAndItem[0])
                tableIndex = tableIndexAndNumbers[0][tableNameIndex]
                if tableAndItem[1] in self.tables[tableIndex].attributes:
                    attributeIndex = self.tables[tableIndex].attributes.index(tableAndItem[1])
                    attributeList = []
                    for item in self.tables[tableIndex].items:
                        attributeList.append(item[attributeIndex])
                    formattedVariables.append(attributeList)
                else:
                    print("!{compareType} is an invalid comparison.".format(compareType = userArgs[2]))
        return formattedVariables

    def MatchItems(self, joinType, displayValues, tableIndexAndNicknames, WhereRequirements):
        #Variables
        longListIndex = None
        shorterListIndex = None
        attrIndex = []
        emptyItem = []
        
        #Nearly done, just need to figure out the outer join stuff. Possibly look for 
        if len(displayValues[0]) != len(displayValues[1]):
            #Determine shorter list
            if len(displayValues[0]) < len(displayValues[1]):
                shorterListIndex = 0
                longListIndex = 1
            else:
                shorterListIndex = 1
                longListIndex = 0
            
        elif "outer" in joinType:
            if "left" in joinType:
                shorterListIndex = 0
                longListIndex = 1

            else:
                shorterListIndex = 1
                longListIndex = 0
                
        if longListIndex != None and shorterListIndex != None:
            #Make empty item for outer joins
            for x in range(0, len(displayValues[shorterListIndex][0])):
                emptyItem.append("")

            #Get attribute index of each filter.
            for item in WhereRequirements:
                if item != WhereRequirements[1]:
                    nicknameAndFilter = item.split(".")
                    tableIndex = tableIndexAndNicknames[0][tableIndexAndNicknames[1].index(nicknameAndFilter[0])]
                    attrIndex.append(self.tables[tableIndex].attributes.index(nicknameAndFilter[1]))

            listSwapped = True
            #cycle through longer list
            while listSwapped == True:
                listSwapped = False
                for longListItem in displayValues[longListIndex]:
                    for shortListItem in displayValues[shorterListIndex]:
                        #If match found, add in same position as long list item
                        if longListItem[attrIndex[longListIndex]] == shortListItem[attrIndex[shorterListIndex]]:
                            if displayValues[longListIndex].index(longListItem) != displayValues[shorterListIndex].index(shortListItem):
                                displayValues[shorterListIndex].insert(displayValues[longListIndex].index(longListItem), shortListItem)
                            break
                        #else add blank elements
                        elif shortListItem == displayValues[shorterListIndex][-1] and joinType != " inner join " and joinType != ", ":
                            displayValues[shorterListIndex].insert(displayValues[longListIndex].index(longListItem), emptyItem)
                            break
                    if len(displayValues[longListIndex]) < len(displayValues[shorterListIndex]):
                        temp = longListIndex
                        longListIndex = shorterListIndex
                        shorterListIndex = temp
                        listSwapped = True
                        break

        return displayValues
    
