#!/usr/bin/python
import subprocess
import json
import os
from gi.repository import Gtk
from LangLoader import LangLoader

class DelDomain(object):

    windowDel = False

    componentName = ["title", "title", "title", "iDesc1", "iDesc2", "domainLbl"]
    component     = []

    def getDelDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/delDomain.glade')

        this.windowDel = mdi.get_object("delDomain")
        this.windowDel.combo = mdi.get_object("informationDomain_domainName")
        this.windowDel.log = mdi.get_object("progressDomain_log")
        this.windowDel.progress = mdi.get_object("progressDomain_progress")

        this.component = LangLoader().initVarForLang("langDel", mdi, this.componentName)

        this.windowDel.show_all()
        mdi.connect_signals(DelHandler(this.windowDel))

class DelHandler(DelDomain):

    domainName = ""

    def __init__(self, window):
        self.window = window
        self.combo  = window.combo
        self.comboData = Gtk.ListStore(str)
        self.defineComboData()
        self.combo.set_model(self.comboData)
        self.cell = Gtk.CellRendererText()
        self.combo.pack_start(self.cell, True)
        self.combo.add_attribute(self.cell, 'text', 0)

    def destroy(self, *args):
        self.window.destroy()

    def prepare(self, w, new_page):
    	cur = self.window.get_current_page()
        print "Current: %s" % cur;
    	if cur == 0:
    		self.window.combo.connect('changed', getCombo, cur)
    	elif cur == 1:
            self.removeDomain()
            self.complete(cur)
        elif cur == 2:
            self.complete(cur)

    def complete(self, stepNumber):
	    self.window.set_page_complete(self.window.get_nth_page(stepNumber), True)

    def removeDomain(self):
        print "Nom de domaine selectionne: %s" % domainName

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

    def defineComboData(self):
        for data in self.loadData(os.path.dirname(__file__) + '/data/domain.dnc'):
            self.comboData.append([data])

    def getCombo(self, uParam):
        index = self.window.combo.get_active()
        model = self.window.combo.get_model()
        domainName = model[index]
        self.complete(uParam)
