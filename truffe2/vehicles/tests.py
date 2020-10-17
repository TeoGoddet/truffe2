# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract

class VehiculesNoLoginTest(TruffeTestAbstract):
    
    def test_home(self):
        self.call_check_redirect('/vehicles/booking/1/pdf/')
    

class VehiculesWithLoginTest(TruffeTestAbstract):
    
    def setUp(self):
        TruffeTestAbstract.setUp(self)
        self.connect_admin()
    
    def test_home(self):
        self.call_check_alert('/vehicles/booking/1/pdf/', alert_expected="")
