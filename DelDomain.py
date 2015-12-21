#!/usr/bin/python
import subprocess
from gi.repository import Gtk

class DelDomain(object):

    windowDel = False

    def getDelDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/delDomain.glade')
        this.windowDel = mdi.get_object("delDomain")
        this.windowDel.show_all()
        mdi.connect_signals(DelHandler(this.windowDel))

class DelHandler(DelDomain):

    def __init__(self, window):
        self.window = window

    def delDomain_destroy(self, *args):
        self.window.destroy()
