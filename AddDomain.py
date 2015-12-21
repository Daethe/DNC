#!/usr/bin/python
import subprocess
import time
import os
from gi.repository import Gtk

class AddDomain(object):

    # mdi = False
    windowAdd = False

    def getAddDomain(this):
        mdi = Gtk.Builder()
        mdi.add_from_file('interface/addDomain.glade')

        this.windowAdd = mdi.get_object("addDomain")
        this.windowAdd.domainName = mdi.get_object("addDomain_informationDomain_domainName")
        this.windowAdd.log = mdi.get_object("addDomain_progressDomain_log")
        this.windowAdd.progress = mdi.get_object("addDomain_progressDomain_progress")

        this.windowAdd.show_all()
        mdi.connect_signals(AddHandler(this.windowAdd))

class AddHandler(AddDomain):

    def __init__(self, window):
        self.window = window

    def addDomain_destroy(self, *args):
        self.window.destroy()

    def addDomain_prepare(self, w, new_page):
    	cur = self.window.get_current_page()
    	if cur == 1:
    		self.window.domainName.connect('changed', self.addDomain_domainName_changed, cur)
    	elif cur == 2:
            self.addDomain_createDomain()
            self.addDomain_complete(cur)
        elif cur == 3:
            self.addDomain_complete(cur)

    def addDomain_complete(self, stepNumber):
	    self.window.set_page_complete(self.window.get_nth_page(stepNumber), True)

    def addDomain_domainName_changed(self, w, uParam):
        self.domainNameText = self.window.domainName.get_text()
        self.addDomain_complete(uParam)

    def addDomain_createDomain(self):
        self.window.log.set_text("Creation des dossiers")
        subprocess.call(["mkdir", "-p", "/var/www/" + self.domainNameText + "/public_html"])
        self.window.progress.set_fraction(0.1)
        subprocess.call(["mkdir", "-p", "/var/www/" + self.domainNameText + "/logs"])
        self.window.progress.set_fraction(0.2)

        self.window.log.set_text("Ajout de la page d'exemple")
        self.addDomain_createDomain_file("file", "/var/www/" + self.domainNameText + "/public_html/index.html", "<html><head><title>Welcome to " + self.domainNameText + "!</title></head><body><h1>Success!  The " + self.domainNameText + " virtual host is working!</h1></body></html>")
        self.window.progress.set_fraction(0.3)

        self.window.log.set_text("Configuration de l'hote virtuel")
        self.addDomain_createDomain_file("file", os.path.dirname(__file__) + "/vhosts/" + self.domainNameText + ".conf", "<VirtualHost *:80>" + "\nServerName " + self.domainNameText + "\nServerAlias www." + self.domainNameText + "\nServerAdmin admin@" + self.domainNameText + "\nDocumentRoot /var/www/" + self.domainNameText + "/public_html/ \nErrorLog /var/www/" + self.domainNameText + "/logs/error.log \nCustomLog /var/www/" + self.domainNameText + "/logs/access.log combined \n</VirtualHost>")
        self.window.progress.set_fraction(0.4)

        subprocess.call(["cp", os.path.dirname(__file__) + "/vhosts/" + self.domainNameText + ".conf", "/etc/apache2/sites-available/" + self.domainNameText + ".conf"])
        self.window.progress.set_fraction(0.5)

        self.window.log.set_text("Activation de l'hote virtuel")
        subprocess.call(["a2ensite", self.domainNameText + ".conf"])
        self.window.progress.set_fraction(0.6)

        self.window.log.set_text("Redemarrage du service apache")
        subprocess.call(["service", "apache2", "restart"])
        self.window.progress.set_fraction(0.7)

        self.window.log.set_text("Ajout des permissions utilisateurs")
        subprocess.call(["chown", "-R", "marc:marc", "/var/www/" + self.domainNameText + "/public_html"])
        self.window.progress.set_fraction(0.8)
        subprocess.call(["chmod", "-R", "755", "/var/www/"])
        self.window.progress.set_fraction(0.9)

        self.window.log.set_text("Ajout de la configuration au fichier hosts")
        subprocess.call(["cp", "/etc/hosts", os.path.dirname(__file__) + "/backup/hosts"])
        self.addDomain_createDomain_file("hosts", "/etc/hosts", "127.0.0.1 " + self.domainNameText)
        self.window.progress.set_fraction(1.0)

        self.window.log.set_text("Nom de domaine pret a l'emploi")

    def addDomain_createDomain_file(self, forFile, path, data):
        data2 = ""
        if forFile == "hosts":
            for line in open(path, "r").readlines():
                data2 = data2 + line
        fo = open(path, "w")
        fo.write(data2 + data)
        fo.close()
