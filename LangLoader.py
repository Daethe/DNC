#!/usr/bin/python
import json

class LangLoader():

    def loadLang(self, window, label):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()
        with open('data/lang/' + data["lang"] + '.json') as data_file:
            data = json.load(data_file)
        return data[window][label]
