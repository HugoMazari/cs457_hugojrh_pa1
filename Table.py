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
            self.name = args[0].split()[1]
            self.location = args[1] + "//" + self.name + self.extension
            os.mkdir(self.location)
            attrAndTypeString = ""
            attrAndType =  args[0].split(" (", 1)[1]
            attrAndType = re.sub("\);(\n|)$", "", attrAndType)
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

    def InsertValues(self, values):
        newItem = []
        eraseAttempt = True
        for type in self.types:
            attrIndex = self.types.index(type)
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

        if eraseAttempt == False:
            self.items.append(newItem)
            self.WriteOrCreateValueFile(newItem, "x")
    
    def WriteOrCreateValueFile(self, values, isCreate):
        newItemString = ""
        for item in values:
            if item == values[-1]:
                    newItemString += "{item}\n".format(item = item)
            else:
                newItemString += "{item} | ".format(item = item)
        templateFile = open(self.location + "//" + "values{valIndex}".format(valIndex = self.items.index(values)) + self.itemExtension, isCreate)
        templateFile.write(newItemString)
        templateFile.close()

    def Where(self, userArgs):
        if userArgs[0] in self.attributes:
            attrIndex = self.attributes.index(userArgs[0])
            if userArgs[1].find("=") != -1:
                comparativeValue = userArgs[2]
                    


                




    #Select
    #Alter