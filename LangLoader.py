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

    def initVarForLang(self, window, mdi, componentName):
        component = []
        # print "===== %s =====" % window
        i = 0
        for name in componentName:
            # print "%s" % name
            if ((window == "langAdd" and name == "title") or (window == "langDel" and name == "title")):
                component.append(mdi.get_object(name + str(i+1)))
                component[i].set_label(LangLoader().loadLang(window, name))
            else:
                component.append(mdi.get_object(name))
                component[i].set_label(LangLoader().loadLang(window, name))
            i = i + 1
        return component
