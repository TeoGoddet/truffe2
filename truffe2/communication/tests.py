# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class CommunicationNoLoginTest(TruffeTestAbstract):
    
    def test_ecrans(self):
        self.call_check_text('/communication/ecrans')

    def test_random_slide(self):
        self.call_check_text('/communication/random_slide')

    def test_website_news(self):
        self.call_check_json('/communication/website_news')

    def test_public_list(self):
        self.call_check_redirect('/communication/logo_public_list')

    def test_logo_public_load(self):
        self.call_check_redirect('/communication/logo_public_load')

    def test_display_search(self):
        self.call_check_redirect('/communication/display/search')


class CommunicationWithLoginTest(TruffeTestAbstract):

    def test_ecrans(self):
        self.call_check_text('/communication/ecrans')

    def test_random_slide(self):
        self.call_check_text('/communication/random_slide')

    def test_website_news(self):
        self.call_check_json('/communication/website_news')

    def test_public_list(self):
        self.call_check_html('/communication/logo_public_list')

    def test_logo_public_load(self):
        self.call_check_text('/communication/logo_public_load', data={"pk":1})

    def test_display_search(self):
        self.call_check_json('/communication/display/search')
        self.call_check_json('/communication/display/search', data={'q':'room'})
        self.call_check_json('/communication/display/search', data={'init':1})
        self.call_check_json('/communication/display/search', data={'unit_pk':2})
