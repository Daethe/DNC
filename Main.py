#!/usr/bin/python
from gi.repository import Gtk
from AddDomain import AddDomain
from DelDomain import DelDomain
from PrefDomain import PrefDomain
from LangLoader import LangLoader

class MainDomain:

    componentName = ["desc1", "desc2", "newDomain", "delDomain", "prefDomain"]
    component = []

    def __init__(self):
        self.mdi = Gtk.Builder()
        self.mdi.add_from_file('interface/mainDomain.glade')
        self.mdi.connect_signals(MainHandler())

        window = self.mdi.get_object("mainDomain")

        self.component = LangLoader().initVarForLang("langMain", self.mdi, self.componentName)
        window.show_all()

class MainHandler:

    def mainDomain_destroy(self, *args):
        Gtk.main_quit(*args)

    def addDomain_opening(self, button):
        AddDomain().getAddDomain()

    def delDomain_opening(self, button):
        DelDomain().getDelDomain()

    def prefDomain_opening(self, button):
        PrefDomain().getPrefDomain()

MainDomain()
Gtk.main()
