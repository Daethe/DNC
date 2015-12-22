#!/usr/bin/python
import subprocess
import json
import os
from gi.repository import Gtk

class DelDomain(object):

    windowDel = False

    def getDelDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/delDomain.glade')
        this.windowDel = mdi.get_object("delDomain")
        this.windowDel.combo = mdi.get_object("delDomain_informationDomain_domainName")
        this.windowDel.show_all()
        mdi.connect_signals(DelHandler(this.windowDel))

class DelHandler(DelDomain):

    def __init__(self, window):
        self.window = window
        self.combo  = window.combo
        self.comboData = Gtk.ListStore(str)
        self.delDomain_defineComboData()
        self.combo.set_model(self.comboData)
        self.cell = Gtk.CellRendererText()
        self.combo.pack_start(self.cell, True)
        self.combo.add_attribute(self.cell, 'text', 0)

    def delDomain_destroy(self, *args):
        self.window.destroy()

    def delDomain_loadData(self, path):
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

    def delDomain_defineComboData(self):
        for data in self.delDomain_loadData(os.path.dirname(__file__) + '/data/domain.dnc'):
            self.comboData.append([data])
