# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract
from django.core.files.uploadedfile import SimpleUploadedFile
from json import dumps


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
        json_file = SimpleUploadedFile("file.json", b'["user1",["user2",1],"user3"]', content_type="text/json")
        self.call_check_text('/members/memberset/1/import')
        self.call_check_text('/members/memberset/1/import', method='post', data={'imported': json_file})

    def test_import_list(self):
        self.call_check_text('/members/memberset/1/import_list')
        self.call_check_text('/members/memberset/1/import_list', method='post', data={"data":"user1\nuser2\nuser3"})

    def test_json(self):
        self.call_check_json('/members/memberset/1/json')

    def test_add(self):
        self.call_check_text('/members/memberset/1/add')
        self.call_check_text('/members/memberset/1/add', method='post', data={'user':'user3'})

    def test_api_v1_info(self):
        self.call_check_text('/members/memberset/1/api/v1/info')
        self.call_check_text('/members/memberset/1/api/v1/info', method='post')

    def test_api_v1(self):
        self.call_check_json('/members/memberset/1/api/v1/', data={'key':'Secret123!'})
        self.assertNotIn('error', self.content)
        self.send_content_type = "application/json"
        self.call_check_json('/members/memberset/1/api/v1/?key=Secret123!', method='post',
                             data=dumps({'members':[{'sciper':'user1', 'payed_fees':12.34}]}))
        self.assertNotIn('error', self.content)
        self.call_check_json('/members/memberset/1/api/v1/?key=Secret123!', method='put',
                             data=dumps({'member':{'sciper':'user1', 'payed_fees':12.34}}))
        self.assertNotIn('error', self.content)
        self.call_check_json('/members/memberset/1/api/v1/?key=Secret123!', method='delete',
                             data=dumps({'member':{'sciper':'user1'}}))
        self.assertNotIn('error', self.content)

    def test_delete(self):
        self.call_check_html('/members/membership/1/delete')
        self.call_check_redirect('/members/membership/1/delete', method='post', redirect_url='/members/memberset/1/')

    def test_toggle_fees(self):
        self.call_check_redirect('/members/membership/1/toggle_fees', redirect_url='/members/memberset/1/')
