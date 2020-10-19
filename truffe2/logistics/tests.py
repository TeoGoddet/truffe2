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
    
    def test_room_search(self):
        self.call_check_json('/logistics/room/search')
        self.call_check_json('/logistics/room/search', data={'q':'room'})
        self.call_check_json('/logistics/room/search', data={'init':1})
        self.call_check_json('/logistics/room/search', data={'unit_pk':2})

    def test_supply_search(self):
        self.call_check_json('/logistics/supply/search')
        self.call_check_json('/logistics/supply/search', data={'q':'room'})
        self.call_check_json('/logistics/supply/search', data={'init':1})
        self.call_check_json('/logistics/supply/search', data={'unit_pk':2})

    def test_loanagreement(self):
        self.call_check_pdf('/logistics/loanagreement/1/pdf/')
