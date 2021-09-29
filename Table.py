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
        self.templateName = "template" + self.extension
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


    #Select
    #Alter