# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class AccountingCoreNoLoginTest(TruffeTestAbstract):
    
    def test_accountingyear_copy(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/copy')

    def test_accountingyear_cost_centers(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/cost_centers')

    def test_accountingyear_accounts(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/accounts')

    def test_accountingyear_get_leaves_cat(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/get_leaves_cat')

    def test_accountingyear_get_parents_cat(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/get_parents_cat')

    def test_accountingyear_get_accounts(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/get_accounts')

    def test_costcenter_available_list(self):
        self.call_check_redirect('/accounting/core/costcenter/available_list')

    def test_account_available_list(self):
        self.call_check_redirect('/accounting/core/account/available_list')

    def test_tva_available_list(self):
        self.call_check_redirect('/accounting/core/tva/available_list')

    def test_unit_users_available_list(self):
        self.call_check_redirect('/accounting/core/unit/1/users_available_list')


class AccountingCoreWithLoginTest(TruffeTestAbstract):

   
    
    def test_accountingyear_copy(self):
        self.call_check_redirect('/accounting/core/accountingyear/1/copy', 
                                 redirect_url='/accounting/core/accountingyear/2/edit')

    def test_accountingyear_cost_centers(self):
        self.call_check_pdf('/accounting/core/accountingyear/1/cost_centers')

    def test_accountingyear_accounts(self):
        self.call_check_pdf('/accounting/core/accountingyear/1/accounts')

    def test_accountingyear_get_leaves_cat(self):
        self.call_check_json('/accounting/core/accountingyear/1/get_leaves_cat')

    def test_accountingyear_get_parents_cat(self):
        self.call_check_json('/accounting/core/accountingyear/1/get_parents_cat')

    def test_accountingyear_get_accounts(self):
        self.call_check_json('/accounting/core/accountingyear/1/get_accounts')

    def test_costcenter_available_list(self):
        self.call_check_json('/accounting/core/costcenter/available_list')

    def test_account_available_list(self):
        self.call_check_json('/accounting/core/account/available_list')

    def test_tva_available_list(self):
        self.call_check_json('/accounting/core/tva/available_list')

    def test_unit_users_available_list(self):
        self.call_check_json('/accounting/core/unit/1/users_available_list')
