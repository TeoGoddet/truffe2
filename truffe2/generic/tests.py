# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class GenericNoLoginTest(TruffeTestAbstract):
    
    def test_check_unit_name(self):
        self.call_check_json('/generic/check_unit_name/', data={'name':'generic'})


class GenericWithLoginTest(TruffeTestAbstract):
    
   
            
    def test_check_unit_name(self):
        self.call_check_json('/generic/check_unit_name/', data={'name':'generic'})
