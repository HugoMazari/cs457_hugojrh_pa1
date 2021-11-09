# Name: Table.py
# Description: Table class implementation
#Author: Hugo
import os
import re

class Table:
    #Constructor
    def __init__(self, args, isFile):
        self.extension = ".htb"
        self.itemExtension = ".hit"
        self.templateName = "template" + self.itemExtension
        self.types = []
        self.attributes = []
        self.items = []
        self.errorVar = "ErroredOut"

        #Table read in from Database Storage
        if(isFile == True):
            self.name = args[0].replace(self.extension,"")
            self.location = args[1] + "//" + args[0]
            templateFile = open(self.location +"//"  + self.templateName, "r")
            attrAndType = templateFile.readline()
            for pair in attrAndType.split(" | "):
                self.IdentifyTypes(pair.split()[1])
                self.attributes.append(pair.split()[0])
            for file in os.listdir(self.location):
                if file.find(self.itemExtension) and file != self.templateName:
                    itemFile = open(self.location +"//" + file, "r")
                    fileContent = itemFile.readline()
                    self.items.append(fileContent.split(" | "))
            #arg = //DatabaseInventory//Database//Table.htb

        #User creates table.
        else:
            self.name = args[0].split()[1].split("(")[0]
            self.location = args[1] + "//" + self.name + self.extension
            os.mkdir(self.location)
            attrAndTypeString = ""
            attrAndType =  args[0].split("(", 1)[1]
            attrAndType = re.sub("\)(\n|)$", "", attrAndType)
            for pair in attrAndType.split(", "):
                self.IdentifyTypes(pair.split()[1])
                self.attributes.append(pair.split()[0])
                attrAndTypeString += ("{tbAttr} {tbType} | ".format(tbAttr = self.attributes[-1], tbType = self.types[-1]))
            attrAndTypeString = re.sub(" \| $", "", attrAndTypeString)
            templateFile = open(self.location + "//" +self.templateName, "x")
            templateFile.write(attrAndTypeString)
            templateFile.close()
            #args = NAME (ATTR TYPE, ATTR TYPE), LOCATION

    #Identify if type used is a recognized type.
    def IdentifyTypes(self, type):
        if re.search("^((var|)char\((\d\d)\)|text)", type.lower()):
            self.types.append(type.lower())
        elif re.search("^((big|small|)int|float)", type.lower()):
            self.types.append(type.lower())
        elif re.search("(money|datetime)", type.lower()):
            self.types.append(type.lower())
        else:
            print("!{typeName} is not a valid type.".format(typeName = type))

    #Insert values to table.
    def InsertValues(self, values):
        newItem = []
        eraseAttempt = True
        attrIndex = 0
        for type in self.types:
            if re.search("^((var|)char\((\d\d)\)|text)", type.lower()):
                if values[attrIndex][0] == "\'" and values[attrIndex][-1] == "\'":
                    if len(values) <= (int(type.split("(")[1].replace(")", ""))) + 2:
                        newItem.append(values[attrIndex].replace("\'",""))
                        if type == self.types[-1]:
                            eraseAttempt = False
                    else:
                        print("!{attemptedValue} is greater than type {attemptedType}."\
                            .format(attemptedValue = values[attrIndex], attemptedType = type))
                        break
                else:
                    print("!{attemptedType} must start and end with quotation marks.".format(attemptedType = type))
                    break
            elif re.search("^(big|small|)int", type.lower()):
                if re.match("^[\d]*$", values[attrIndex]):
                    newItem.append(values[attrIndex])
                    if type == self.types[-1]:
                        eraseAttempt = False
                else:
                    print("{attemptedType} must be an integer.".format(attemptedType = type))
                    break
            elif type.lower() == "float":
                if re.match("^[\d]*.[\d]*$", values[attrIndex]):
                    newItem.append(values[attrIndex])
                    if type == self.types[-1]:
                        eraseAttempt = False
                else:
                    print("{attemptedType} must have a decimal point.".format(attemptedType = type))
                    break
            else:
                newItem.append(values[attrIndex])
                if type == self.types[-1]:
                    eraseAttempt = False
            attrIndex += 1

        if eraseAttempt == False:
            self.items.append(newItem)
            self.WriteOrCreateValueFile(newItem, "x")
    
    #Writes or creates values to a file.
    def WriteOrCreateValueFile(self, values, isCreate):
        newItemString = ""
        fileName = ""
        for item in values:
            if item == values[-1]:
                    newItemString += "{item}\n".format(item = item)
            else:
                newItemString += "{item} | ".format(item = item)
            fileName += item
        while os.path.exists(self.location + "//" + fileName + self.itemExtension) and isCreate == 'x':
                if "_" in fileName:
                    copyVersion = fileName.split("_")[1]
                    fileName = fileName.replace("_{version}".format(version = copyVersion), "_{version}".format(verion = str(int(copyVersion) + 1)))
                else:
                    fileName += "_1"
        templateFile = open(self.location + "//" + fileName + self.itemExtension, isCreate)
        templateFile.write(newItemString)
        templateFile.close()

    #Determine which values to display.
    def Where(self, userArgs):
        filteredItems = []
        if userArgs[0] in self.attributes:
            attrIndex = self.attributes.index(userArgs[0])
            comparativeValue = userArgs[2].replace("\'","")
            for item in self.items:
                if userArgs[1] == "=":
                    if item[attrIndex] == comparativeValue:
                        filteredItems.append(item)
                    else:
                        set(comparativeValue).symmetric_difference(set(item[attrIndex]))
                elif userArgs[1] == "!=":
                    if str(item[attrIndex]) != comparativeValue:
                        filteredItems.append(item)
                elif userArgs[1] == "<":
                    if re.match("^[\d]*.[\d]*$", item[attrIndex]):
                        if re.match("^[\d]*.[\d]*$", comparativeValue):
                            if float(item[attrIndex]) < float(comparativeValue):
                                filteredItems.append(item)
                elif userArgs[1] == ">":
                    if re.match("^[\d]*.[\d]*$", item[attrIndex]):
                        if re.match("^[\d]*.[\d]*$", comparativeValue):
                            if float(item[attrIndex]) > float(comparativeValue):
                                filteredItems.append(item)
                elif userArgs[1] == "<=":
                    if re.match("^[\d]*.[\d]*$", item[attrIndex]):
                        if re.match("^[\d]*.[\d]*$", comparativeValue):
                            if float(item[attrIndex]) < float(comparativeValue):
                                filteredItems.append(item)
                elif userArgs[1] == ">=":
                    if re.match("^[\d]*.[\d]*$", item[attrIndex]):
                        if re.match("^[\d]*.[\d]*$", comparativeValue):
                            if float(item[attrIndex]) < float(comparativeValue):
                                filteredItems.append(item)
                else:
                    print("!{compareType} is an invalid comparison.".format(compareType = userArgs[1]))
        return filteredItems

    #modifies values in the table
    def ModifyValues(self, targets, attrTarget, newVal):
        for target in targets:
            oldFile = ""
            for values in target:
                oldFile += values
            targetIndex = self.items.index(target)
            attrIndex = self.attributes.index(attrTarget)
            self.items[targetIndex][attrIndex] = newVal
            self.WriteOrCreateValueFile(self.items[targetIndex],"x")
            
            os.remove(self.location + "//" + oldFile + self.itemExtension)

    #Select
    #Alter