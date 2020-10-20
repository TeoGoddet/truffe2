# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeCmdTestAbstract
from users.models import TruffeUser


class TruffeCommandsTest(TruffeCmdTestAbstract):

    def setUp(self):
        TruffeCmdTestAbstract.setUp(self)
        TruffeUser.objects.create_superuser(username='179189', password='admin', first_name='179189', last_name='179189')
        TruffeUser.objects.create_superuser(username='185952', password='admin', first_name='185952', last_name='185952')

    def test_export_accreds(self):
        self.call_command()
        
    def test_export_users(self):
        self.call_command()
        
    def test_import_accreds(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_compta(self):
        self.filein.write(u'{"lignes":[], "errors":[]}')
        self.call_command()
        
    def test_import_creditcard(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_financesglob(self):
        self.filein.write(u'{"year":[]}')
        self.call_command()
        
    def test_import_jdcs(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_matos(self):
        self.filein.write(u'{"materiel":[], "reservations":[]}')
        self.call_command()
        
    def test_import_members(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_ndfs(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_rcashs(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_rooms(self):
        self.filein.write(u'{"rooms":[], "reservations":[]}')
        self.call_command()
        
    def test_import_subventions(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_users(self):
        self.filein.write(u'{"data":[]}')
        self.call_command()
        
    def test_import_vehicles(self):
        self.filein.write(u'{"providers":[], "cards":[], "types":[], "places":[], "booking":[]}')
        self.call_command()
