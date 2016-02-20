#!/usr/bin/python
import subprocess
import json
import os
from gi.repository import Gtk
from LangLoader import LangLoader

class PrefDomain(object):

    windowPref = False

    componentName = ["langTitle", "dbTitle", "hostLbl", "portLbl", "userLbl", "passLbl", "dbDesc", "cancel", "save"]
    component = []

    def getPrefDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/prefDomain.glade')

        this.windowPref = mdi.get_object("prefDomain")
        this.windowPref.comboLang  = mdi.get_object("langSe")
        this.windowPref.comboDb    = mdi.get_object("dbType")

        this.windowPref.host   = mdi.get_object("hostDb")
        this.windowPref.port   = mdi.get_object("portDb")
        this.windowPref.userw  = mdi.get_object("userDb")
        this.windowPref.passw  = mdi.get_object("passDb")

        this.component = LangLoader().initVarForLang("langPref", mdi, this.componentName)

        this.windowPref.show_all()

        mdi.connect_signals(PrefHandler(this.windowPref))

class PrefHandler(PrefDomain):

    def __init__(self, window):
        self.window = window

        self.lang = ""
        self.db   = ""

        self.comboLang  = window.comboLang
        self.comboLangData = Gtk.ListStore(str)
        self.defineComboData(1)
        self.comboLang.set_model(self.comboLangData)
        self.cell = Gtk.CellRendererText()
        self.comboLang.pack_start(self.cell, True)
        self.comboLang.add_attribute(self.cell, 'text', 0)

        self.comboDb  = window.comboDb
        self.comboDbData = Gtk.ListStore(str)
        self.defineComboData(2)
        self.comboDb.set_model(self.comboDbData)
        self.cell = Gtk.CellRendererText()
        self.comboDb.pack_start(self.cell, True)
        self.comboDb.add_attribute(self.cell, 'text', 0)

        self.setTextbox()
        self.setComboBox(self.lang, self.db)

    def destroy(self, *args):
        self.window.destroy()

    def save(self, *args):
        self.save_file(
            self.getItem(self.window.comboLang)[0],
            self.getItem(self.window.comboDb)[0],
            self.window.host.get_text(),
            self.window.port.get_text(),
            self.window.userw.get_text(),
            self.window.passw.get_text()
        )
        self.destroy()

    def save_file(self, lang, db, host, port, user, password):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()

        data["lang"] = lang
        data["dbTy"] = db
        data["host"] = host
        data["port"] = port
        data["user"] = user
        data["pass"] = password

        jsonFile = open("data/pref.dnc", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

    def loadData(self, path):
        data = ""
        fo = open(path, "r")
        lines = fo.readlines()
        i = 0
        for line in lines:
            if i == len(lines) - 1:
                data = data + line
            elif i != len(lines) - 1:
                data = data + line + ":"
            i = i + 1
        return data.replace('\n', '').split(":")

    def defineComboData(self, i):
        if i == 1:
            for data in self.loadData(os.path.dirname(__file__) + '/data/lang.dnc'):
                self.comboLangData.append([data])
        elif i == 2:
            self.comboDbData.append(["Mysql"])
            self.comboDbData.append(["PostgreSQL"])

    def setTextbox(self):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()

        self.lang = data["lang"]
        self.db   = data["dbTy"]

        self.window.host.set_text(data["host"])
        self.window.port.set_text(data["port"])
        self.window.userw.set_text(data["user"])
        self.window.passw.set_text(data["pass"])

    def setComboBox(self, lang, db):
        self.window.comboLang.set_active(self.getActiveItem(self.window.comboLang, self.lang))
        self.window.comboDb.set_active(self.getActiveItem(self.window.comboDb, self.db))

    def getItem(self, combo):
        index = combo.get_active()
        model = combo.get_model()
        return model[index]

    def getActiveItem(self, combo, data):
        i = 0
        m = combo.get_model()
        while m[i][0] != data :
            i = i + 1
        return i;
