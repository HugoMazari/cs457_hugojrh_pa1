from Table import Table
import os

class Database:
    def __init__(self, args, isFile):
        self.extension = ".hdb"
        self.tables = []
        self.tableNames = []
        tables = []

        if isFile:
            self.name = args[0].replace(self.extension, "")
            self.location = args[1] + "//" + args[0]
            allTables = os.listdir(self.location)
            for table in allTables:
                self.tables.append(Table([table, self.location], True))
                self.tableNames.append(self.tables[-1].name)

        else:
            self.name = args[0].split(";")[0]
            self.location = self.CreateDatabase(args[1] + "//")
            

    def CreateDatabase(self, databaseInventory):
        os.mkdir(databaseInventory + self.name + self.extension)
        return databaseInventory + self.name + self.extension

    def OpenTables(self):
        for dir, subdirs, file in os.walk(self.location):
            for table in subdirs:
                self.tables.append(Table([table, dir], True))
        for table in self.tables:
            self.tablesNames.append(table.name)
        
    def CreateTable(self, userArgs):
        if userArgs.split()[1].replace(";","") in self.tableNames:
                print("!Failed to create database {dbName} because it already exists.".format(dbName = userArgs.split()[1].replace(";","")))
        else:
            self.tables.append(Table([userArgs, self.location], False))
            self.tableNames.append(self.tables[-1].name)