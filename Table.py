import os
import re
import Types

class Table:
    def __init__(self, args, isFile):
        self.extension = ".htb"
        self.itemExtension = ".hit"
        self.templateName = "template" + self.extension
        self.types = []
        self.attributes = []
        self.items = []

        if(isFile == True):
            print("From the file reader.")
            self.name = args.split("//")[-1].replace(self.extension,"")
            self.location = args.replace(self.Name + self.extension, "")
            #arg = //DatabaseInventory//Database//Table.htb

        #User creates table.
        else:
            self.name = args[0].split()[1]
            attrAndType =  args[0].split(" (", 1)[1]
            attrAndType = re.sub("\);$", "", attrAndType)
            for pair in attrAndType.split(", "):
                self.types.append(pair.split()[1])
                self.attributes.append(pair.split()[0])
            self.location = args[1] + "//" + self.name + self.extension
            os.mkdir(self.location)
            #args = NAME (ATTR TYPE, ATTR TYPE), LOCATION        



    #Create
    #Drop
    #Select
    #Alter