# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract
from django.db.utils import OperationalError


class MainNoLoginTest(TruffeTestAbstract):
    
    def test_home(self):
        self.call_check_redirect('/')
        
    def test_get_to_moderate(self):
        self.call_check_redirect('/get_to_moderate')

    def test_link_base(self):
        self.call_check_redirect('/link/base')

    def test_last_100_logging_entries(self):
        self.call_check_redirect('/last_100_logging_entries')

    def test_search(self):
        self.call_check_redirect('/search/')

    def test_set_homepage(self):
        self.call_check_redirect('/set_homepage')

    def test_file_download_list(self):
        self.call_check_redirect('/file/download_list/')

    def test_file_download(self):
        self.call_check_redirect('/file/download/1')

    def test_signabledocument_download(self):
        self.call_check_redirect('/signabledocument/download/1')

    def test_signabledocument_sign(self):
        self.call_check_redirect('/signabledocument/sign/1')

    def test_signabledocument_signs(self):
        self.call_check_redirect('/signabledocument/signs/')


class MainWithLoginTest(TruffeTestAbstract):
    
    login_username = 'admin'
    
    def test_home(self):
        self.call_check_html('/')
        
    def test_get_to_moderate(self):
        self.call_check_text('/get_to_moderate')

    def test_link_base(self):
        self.call_check_html('/link/base')
 
    def test_last_100_logging_entries(self):
        # TODO : problem of SQL ('UNION' syntax) to show the action '/last_100_logging_entries'
        with self.assertRaises(OperationalError) as context:
            self.call_check_html('/last_100_logging_entries')
        self.assertEqual(str(context.exception), 'near "UNION": syntax error')
 
    def test_search(self):
        self.call_check_html('/search/')
 
    def test_set_homepage(self):
        self.call_check_text('/set_homepage')
 
    def test_file_download_list(self):
        self.call_check_html('/file/download_list/', {'group':'misc'})
 
    def test_file_download(self):
        self.call_check_text('/file/download/1')
 
    def test_signabledocument_download(self):
        self.call_check_text('/signabledocument/download/1')
 
    def test_signabledocument_sign(self):
        self.call_check_html('/signabledocument/sign/2')
 
    def test_signabledocument_signs(self):
        self.call_check_html('/signabledocument/signs/')


class MainWithLog1Test(TruffeTestAbstract):

    login_username = 'user1'
    
    def test_home(self):
        self.call_check_html('/')


class MainWithLog2Test(TruffeTestAbstract):

    login_username = 'user2'
    
    def test_home(self):
        self.call_check_html('/')


class MainWithLog3Test(TruffeTestAbstract):

    login_username = 'user3'
    
    def test_home(self):
        self.call_check_html('/')
