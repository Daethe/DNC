#!/usr/bin/python
from gi.repository import Gtk
from AddDomain import AddDomain
from DelDomain import DelDomain
from PrefDomain import PrefDomain
from LangLoader import LangLoader

class MainDomain:

    def __init__(self):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/mainDomain.glade')
        mdi.connect_signals(MainHandler())

        window = mdi.get_object("mainDomain")

        window.desc1     = mdi.get_object("mainDomain_desc1")
        window.desc2     = mdi.get_object("mainDomain_desc2")
        window.addDomain = mdi.get_object("newDomain")
        window.delDomain = mdi.get_object("delDomain")
        window.pref      = mdi.get_object("preference")

        window.desc1.set_label(LangLoader().loadLang("langMain", "desc1"))
        window.desc2.set_label(LangLoader().loadLang("langMain", "desc2"))
        window.addDomain.set_label(LangLoader().loadLang("langMain", "newDomain"))
        window.delDomain.set_label(LangLoader().loadLang("langMain", "delDomain"))
        window.pref.set_label(LangLoader().loadLang("langMain", "prefDomain"))

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
