#!/usr/bin/python
from gi.repository import Gtk
from AddDomain import AddDomain
from DelDomain import DelDomain

class MainDomain:

    def __init__(self):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/mainDomain.glade')
        mdi.connect_signals(MainHandler())

        window = mdi.get_object("mainDomain")
        window.show_all()

class MainHandler:

    def mainDomain_destroy(self, *args):
        Gtk.main_quit(*args)

    def addDomain_opening(self, button):
        AddDomain().getAddDomain()

    def delDomain_opening(self, button):
        DelDomain().getDelDomain()

MainDomain()
Gtk.main()
