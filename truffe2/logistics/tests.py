# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class LogisticsNoLoginTest(TruffeTestAbstract):
    
    def test_room_search(self):
        self.call_check_redirect('/logistics/room/search')

    def test_supply_search(self):
        self.call_check_redirect('/logistics/supply/search')

    def test_loanagreement(self):
        self.call_check_redirect('/logistics/loanagreement/1/pdf/')


class LogisticsWithLoginTest(TruffeTestAbstract):
    
    def setUp(self):
        TruffeTestAbstract.setUp(self)
        self.connect_admin()
    
    def test_room_search(self):
        self.call_check_alert('/logistics/room/search',alert_expected="")

    def test_supply_search(self):
        self.call_check_alert('/logistics/supply/search',alert_expected="")

    def test_loanagreement(self):
        self.call_check_alert('/logistics/loanagreement/1/pdf/',alert_expected="")
