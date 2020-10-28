# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract, TruffeCmdTestAbstract


class NotificationsNoLoginTest(TruffeTestAbstract):
    
    def test_dropdown(self):
        self.call_check_redirect('/notifications/dropdown')

    def test_goto(self):
        self.call_check_redirect('/notifications/goto/1')

    def test_center(self):
        self.call_check_redirect('/notifications/center/')

    def test_center_keys(self):
        self.call_check_redirect('/notifications/center/keys')

    def test_center_json(self):
        self.call_check_redirect('/notifications/center/json')

    def test_center_restrictions(self):
        self.call_check_redirect('/notifications/center/restrictions')

    def test_center_restrictions_update(self):
        self.call_check_redirect('/notifications/center/restrictions/update')

    def test_read(self):
        self.call_check_redirect('/notifications/read')


class NotificationsWithLoginTest(TruffeTestAbstract):
    
    login_username = 'admin'
    
    def test_dropdown(self):
        self.call_check_text('/notifications/dropdown', data={'read':1, 'allread':1})

    def test_goto(self):
        self.call_check_redirect('/notifications/goto/1', data={"next":'/'}, redirect_url='/')

    def test_center(self):
        self.call_check_html('/notifications/center/')

    def test_center_keys(self):
        self.call_check_text('/notifications/center/keys')

    def test_center_json(self):
        self.call_check_json('/notifications/center/json')

    def test_center_restrictions(self):
        self.call_check_text('/notifications/center/restrictions', data={'current_type':'mynotifkey'})

    def test_center_restrictions_update(self):
        self.call_check_text('/notifications/center/restrictions/update', data={'current_type':'mynotifkey'})

    def test_read(self):
        self.call_check_text('/notifications/read', data={'pk':1})


class NotificationsCommandsTest(TruffeCmdTestAbstract):
    
    def test_create_notifications_templates(self):
        self.call_command("test_create", "drafted")
        
    def test_process_notifications(self):
        self.call_command()
    
