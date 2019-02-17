#! /usr/bin/python3
#Daniel McCarthy 04/2018
#author: Kiet Lam
#This file contains code to manage the configuration file
import json

class Config():
    def __init__(self, ConfigFileName):
        self.FileName = ConfigFileName #Name of the configfile we write/read
        self.Config = ''#readconfig
        self.Sources = {}

    def SourceAdd(self, Address, SourceName, DriverName): #Called whenever we add a data source to the system
        #print("Added Source: {0}".format(SourceName))
        if (SourceName not in self.Sources): #Check if sane
            self.Sources[SourceName] = {'Address' : Address, 'DriverName' : DriverName, 'Tags' : {}} #Add Source Dict to Dict
            self.WriteJSON()

    def SourceDel(self, SourceName): #Called whenever we delete a data source from the system
        print("Removed Source: {0}".format(SourceName))

    def TagSet(self, SourceName, TagName, Mode, Interval):  #Called whenever we add or modify a Tag
        #print("Added Tag: {0}/{1}".format(SourceName, TagName))
        if (SourceName in self.Sources): #Check if sane
            self.Sources[SourceName]["Tags"][TagName] = {'Mode' : Mode, 'Interval' : Interval} #Add Tag Dict to Dict
            self.WriteJSON()

    def TagDel(self, SourceName, TagName): #Called whenever we remove a Tag
        print("Removed Tag: {0}/{1}".format(SourceName, TagName))

    def Set(self, Manager):
        print("Set from config file")
        #e.g:
        #for source in sources
        #Manager.AddSource()
        #Manager.AddTag()
        #And so on

    def WriteJSON(self):
        configFile = ''
        checkPrimarySet = False
        checkKeySet = False
        checkAddress = False
        checkDriver = False
        checkTagNames = False
        checkMode = False
        checkInterval = False
        newEntry = ''

        try:
            #Check Config.Sources.items contain attributes in TagNames
            for x in Config.Sources.items():
                if not x[1]["Tags"]:
                    continue
                else:
                    checkTagNames = True
                    #Load current configuration file
                    with open('ConfigFile.txt') as json_data:
                        configFile = json.load(json_data)
                    json_data.close()

            #Attributes in TagName is not empty
            if checkTagNames:

                checkKeySet = Config.KeySetCheck(configFile)

                if(checkKeySet):

                    checkDriver = Config.DriverCheck(configFile)
                    checkAddress = Config.AddressCheck(configFile)
                    checkInterval = Config.IntervalCheck(configFile)
                    checkMode = Config.ModeCheck(configFile)

                    if(checkDriver == False or checkAddress == False
                       or checkInterval == False or checkMode == False):
                       print("Begin write to file...")

                       for x in Config.Sources:
                           for j in Config.Sources.items():
                               i = j[1]["Tags"]
                               for h in i:
                                   for g in i.items():
                                       newEntry = {x :{"DriverName":j[1]["DriverName"], "Address": j[1]["Address"], "Tags":{h:{"Interval":g[1]["Interval"],"Mode":g[1]["Mode"]}}}}
                                       configFile.append(newEntry)

                       size = len(configFile)
                       file = open("ConfigFile.txt","w")
                       file.write("[")
                       for x in configFile:
                               file.write(json.dumps(x))
                               size = size-1
                               if size > 1:
                                   file.write(",")
                                   file.write("\n")
                               if size == 1:
                                   file.write(",")
                                   file.write("\n")
                       file.write("]")
                       file.close()
                       print("Write to file completed...")
                    else:
                        print("No entry made...")
                else:
                    print("Begin write to file...")

                    for x in Config.Sources:
                        for j in Config.Sources.items():
                            i = j[1]["Tags"]
                            for h in i:
                                for g in i.items():
                                    newEntry = {x :{"DriverName":j[1]["DriverName"], "Address": j[1]["Address"], "Tags":{h:{"Interval":g[1]["Interval"],"Mode":g[1]["Mode"]}}}}
                                    configFile.append(newEntry)

                    size = len(configFile)
                    file = open("ConfigFile.txt","w")
                    file.write("[")
                    for x in configFile:
                        file.write(json.dumps(x))
                        size = size-1
                        if size > 1:
                            file.write(",")
                            file.write("\n")
                        if size == 1:
                            file.write(",")
                            file.write("\n")
                    file.write("]")
                    file.close()
                    print("Write completed...")
        except:
            print("401 System Error...")

    def KeySetCheck(self, configFile):
        for tagSetKey in configFile:
            tagNameKey = tagSetKey
            for tagKey in tagNameKey:
                for primaryKey in Config.Sources:
                    if tagKey == primaryKey:
                        return True
        return False #Means the child's key does not match the father's key
                     #New entry for KeySet and Everything else.
    def DriverCheck(self, configFile):

        temp = ''

        for x in configFile:
            temp = x
            for y in temp:
                for j in Config.Sources:
                    if y == j:
                        for g in temp.items():
                            for h in Config.Sources.items():
                                if(h[1]["DriverName"] == g[1]["DriverName"]):
                                    return True
        return False

    def AddressCheck(self, configFile):

        temp = ''

        for x in configFile:
            temp = x
            for y in temp:
                for j in Config.Sources:
                    if y == j:
                        for g in temp.items():
                            for h in Config.Sources.items():
                                if(h[1]["Address"] == g[1]["Address"]):
                                    return True
        return False


    def IntervalCheck(self, configFile):

        temp = ''

        for x in configFile:
            temp = x
            for y in temp:
                for j in Config.Sources:
                    if y == j:
                        for g in temp.items():
                            for h in Config.Sources.items():
                                k = g[1]["Tags"]
                                f = h[1]["Tags"]
                                for d in k:
                                    for w in f:
                                        if(d == w):
                                            for g in f.items():
                                                for n in k.items():
                                                    if(g[1]["Interval"] == n[1]["Interval"]):
                                                        return True
        return False

    def ModeCheck(self, configFile):

        temp = ''

        for x in configFile:
            temp = x
            for y in temp:
                for j in Config.Sources:
                    if y == j:
                        for g in temp.items():
                            for h in Config.Sources.items():
                                k = g[1]["Tags"]
                                f = h[1]["Tags"]
                                for d in k:
                                    for w in f:
                                        if(d == w):
                                            for g in f.items():
                                                for n in k.items():
                                                    if(g[1]["Mode"] == n[1]["Mode"]):
                                                        return True
        return False

    def Read(self):

        j = open('ConfigFile.txt')

        data = json.load(j)

        for a in data:
            Config = a
            for b in Config:
                for x in Config.items():
                    g = x[1]["Tags"]
                    for y in g.items():
                        print("TagKeys: " + b + ", Driver name: " + x[1]["DriverName"] + ", Address: " + x[1]["Address"] + ", TagNames: " + x[0] +", Mode: " + y[1]["Mode"] + ", Interval: " + str(y[1]["Interval"]))


if __name__ == "__main__":
    Config = Config('')
    Config.SourceAdd("127.0.0.7", "PLC7", "drv-dummy2.py")
    Config.TagSet("PLC7", "Tag7", "change", 80)
    #Config.Read()
