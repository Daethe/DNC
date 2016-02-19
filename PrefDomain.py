#!/usr/bin/python
import subprocess
import json
import os
from gi.repository import Gtk
from LangLoader import LangLoader

class PrefDomain(object):

    windowPref = False

    def getPrefDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/prefDomain.glade')

        this.windowPref = mdi.get_object("prefDomain")
        this.windowPref.comboLang  = mdi.get_object("prefDomain_langSe")
        this.windowPref.comboDb    = mdi.get_object("prefDomain_dbType")

        this.windowPref.langT  = mdi.get_object("prefDomain_langTitle")
        this.windowPref.dbT    = mdi.get_object("prefDomain_dbTitle")
        this.windowPref.hostLb = mdi.get_object("prefDomain_hostLbl")
        this.windowPref.portLb = mdi.get_object("prefDomain_portLbl")
        this.windowPref.userLb = mdi.get_object("prefDomain_userLbl")
        this.windowPref.passLb = mdi.get_object("prefDomain_passLbl")
        this.windowPref.desc   = mdi.get_object("prefDomain_dbDesc")

        this.windowPref.host   = mdi.get_object("prefDomain_hostDb")
        this.windowPref.port   = mdi.get_object("prefDomain_portDb")
        this.windowPref.userw  = mdi.get_object("prefDomain_userDb")
        this.windowPref.passw  = mdi.get_object("prefDomain_passDb")

        this.windowPref.langT .set_label(LangLoader().loadLang("langPref", "langTitle"))
        this.windowPref.dbT   .set_label(LangLoader().loadLang("langPref", "dbTitle"))
        this.windowPref.hostLb.set_label(LangLoader().loadLang("langPref", "hostLbl"))
        this.windowPref.portLb.set_label(LangLoader().loadLang("langPref", "portLbl"))
        this.windowPref.userLb.set_label(LangLoader().loadLang("langPref", "userLbl"))
        this.windowPref.passLb.set_label(LangLoader().loadLang("langPref", "passLbl"))
        this.windowPref.desc  .set_label(LangLoader().loadLang("langPref", "dbDesc"))

        this.windowPref.show_all()

        mdi.connect_signals(PrefHandler(this.windowPref))

class PrefHandler(PrefDomain):

    def __init__(self, window):
        self.window = window

        self.lang = ""
        self.db   = ""

        self.comboLang  = window.comboLang
        self.comboLangData = Gtk.ListStore(str)
        self.prefDomain_defineComboData(1)
        self.comboLang.set_model(self.comboLangData)
        self.cell = Gtk.CellRendererText()
        self.comboLang.pack_start(self.cell, True)
        self.comboLang.add_attribute(self.cell, 'text', 0)

        self.comboDb  = window.comboDb
        self.comboDbData = Gtk.ListStore(str)
        self.prefDomain_defineComboData(2)
        self.comboDb.set_model(self.comboDbData)
        self.cell = Gtk.CellRendererText()
        self.comboDb.pack_start(self.cell, True)
        self.comboDb.add_attribute(self.cell, 'text', 0)

        self.prefDomain_setTextbox()
        self.prefDomain_setComboBox(self.lang, self.db)

    def prefDomain_destroy(self, *args):
        self.window.destroy()

    def prefDomain_save(self, *args):
        self.prefDomain_save_file(
            self.prefDomain_getItem(self.window.comboLang)[0],
            self.prefDomain_getItem(self.window.comboDb)[0],
            self.window.host.get_text(),
            self.window.port.get_text(),
            self.window.userw.get_text(),
            self.window.passw.get_text()
        )
        self.prefDomain_destroy()

    def prefDomain_save_file(self, lang, db, host, port, user, password):
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

    def prefDomain_loadData(self, path):
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

    def prefDomain_defineComboData(self, i):
        if i == 1:
            for data in self.prefDomain_loadData(os.path.dirname(__file__) + '/data/lang.dnc'):
                self.comboLangData.append([data])
        elif i == 2:
            self.comboDbData.append(["Mysql"])
            self.comboDbData.append(["PostgreSQL"])

    def prefDomain_setTextbox(self):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()

        self.lang = data["lang"]
        self.db   = data["dbTy"]

        self.window.host.set_text(data["host"])
        self.window.port.set_text(data["port"])
        self.window.userw.set_text(data["user"])
        self.window.passw.set_text(data["pass"])

    def prefDomain_setComboBox(self, lang, db):
        self.window.comboLang.set_active(self.prefDomain_getActiveItem(self.window.comboLang, self.lang))
        self.window.comboDb.set_active(self.prefDomain_getActiveItem(self.window.comboDb, self.db))

    def prefDomain_getItem(self, combo):
        index = combo.get_active()
        model = combo.get_model()
        return model[index]

    def prefDomain_getActiveItem(self, combo, data):
        i = 0
        m = combo.get_model()
        while m[i][0] != data :
            i = i + 1
        return i;
