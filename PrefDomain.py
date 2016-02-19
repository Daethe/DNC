#!/usr/bin/python
import subprocess
import json
import os
from gi.repository import Gtk

class PrefDomain(object):

    windowPref = False

    def getPrefDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/prefDomain.glade')
        this.windowPref = mdi.get_object("prefDomain")
        this.windowPref.combo  = mdi.get_object("lang_combobox")
        this.windowPref.host   = mdi.get_object("prefDomain_hostMysql")
        this.windowPref.port   = mdi.get_object("prefDomain_portMysql")
        this.windowPref.passw  = mdi.get_object("prefDomain_passMysql")
        this.windowPref.show_all()
        mdi.connect_signals(PrefHandler(this.windowPref))

class PrefHandler(PrefDomain):

    def __init__(self, window):
        self.window = window

        self.combo  = window.combo
        self.comboData = Gtk.ListStore(str)
        self.prefDomain_defineComboData()
        self.combo.set_model(self.comboData)
        self.cell = Gtk.CellRendererText()
        self.combo.pack_start(self.cell, True)
        self.combo.add_attribute(self.cell, 'text', 0)

        self.prefDomain_setTextbox()

    def prefDomain_destroy(self, *args):
        self.window.destroy()

    def prefDomain_save(self, *args):
        index = self.window.combo.get_active()
        model = self.window.combo.get_model()
        item = model[index]

        hostMysql = self.window.host.get_text()
        portMysql = self.window.port.get_text()
        passMysql = self.window.passw.get_text()

        self.prefDomain_save_file(item[0], hostMysql, portMysql, passMysql)
        self.prefDomain_destroy()

    def prefDomain_save_file(self, lang, host, port, password):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()

        data["lang"] = lang
        data["host"] = host
        data["port"] = port
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

    def prefDomain_defineComboData(self):
        for data in self.prefDomain_loadData(os.path.dirname(__file__) + '/data/lang.dnc'):
            self.comboData.append([data])

    def prefDomain_setTextbox(self):
        jsonFile = open("data/pref.dnc", "r")
        data = json.load(jsonFile)
        jsonFile.close()
        self.window.host.set_text(data["host"])
        self.window.port.set_text(data["port"])
        self.window.passw.set_text(data["pass"]) 
