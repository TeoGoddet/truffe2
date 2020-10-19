# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class MembersNoLoginTest(TruffeTestAbstract):

    def test_export(self):
        self.call_check_redirect('/members/memberset/1/export')

    def test_import(self):
        self.call_check_redirect('/members/memberset/1/import')

    def test_import_list(self):
        self.call_check_redirect('/members/memberset/1/import_list')

    def test_json(self):
        self.call_check_redirect('/members/memberset/1/json')

    def test_add(self):
        self.call_check_redirect('/members/memberset/1/add')

    def test_api_v1_info(self):
        self.call_check_redirect('/members/memberset/1/api/v1/info')

    def test_api_v1(self):
        self.call_check_json('/members/memberset/1/api/v1/', data={'key':'Secret123!'})

    def test_delete(self):
        self.call_check_redirect('/members/membership/1/delete')

    def test_toggle_fees(self):
        self.call_check_redirect('/members/membership/1/toggle_fees')


class MembersWithLoginTest(TruffeTestAbstract):

   

    def test_export(self):
        self.call_check_json('/members/memberset/1/export')

    def test_import(self):
        self.call_check_text('/members/memberset/1/import')

    def test_import_list(self):
        self.call_check_text('/members/memberset/1/import_list')

    def test_json(self):
        self.call_check_json('/members/memberset/1/json')

    def test_add(self):
        self.call_check_text('/members/memberset/1/add')

    def test_api_v1_info(self):
        self.call_check_text('/members/memberset/1/api/v1/info')

    def test_api_v1(self):
        self.call_check_json('/members/memberset/1/api/v1/', data={'key':'Secret123!'})

    def test_delete(self):
        self.call_check_html('/members/membership/1/delete')

    def test_toggle_fees(self):
        self.call_check_redirect('/members/membership/1/toggle_fees', redirect_url='/members/memberset/1/')
