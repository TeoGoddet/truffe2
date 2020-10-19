# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract
from re import match


class AccountingMainNoLoginTest(TruffeTestAbstract):
    
    def test_accounting_graph(self):
        self.call_check_redirect('/accounting/main/accounting/graph/')

    def test_accounting_errors_send_message(self):
        self.call_check_redirect('/accounting/main/accounting/errors/send_message/1')

    def test_accounting_import_step0(self):
        # TODO : no '@login_required' for this view
        self.call('/accounting/main/accounting/import/step/0', status_expected=404)

    def test_accounting_import_step1(self):
        self.call_check_redirect('/accounting/main/accounting/import/step/1/1')

    def test_accounting_import_step2(self):
        self.call_check_redirect('/accounting/main/accounting/import/step/2/1')

    def test_budget_available_list(self):
        self.call_check_redirect('/accounting/main/budget/available_list'),

    def test_budget_copy(self):
        self.call_check_redirect('/accounting/main/budget/1/copy')

    def test_budget_get_infos(self):
        self.call_check_redirect('/accounting/main/budget/1/get_infos')

    def test_budget_pdf(self):
        self.call_check_redirect('/accounting/main/budget/1/pdf/'),

    def test_accounting_budget_view(self):
        self.call_check_redirect('/accounting/main/accounting/budget_view'),


class AccountingMainWithLoginTest(TruffeTestAbstract):
    
   
    
    def test_accounting_graph(self):
        self.call_check_text('/accounting/main/accounting/graph/', data={'costcenter':1})

    def test_accounting_errors_send_message(self):
        self.call_check_text('/accounting/main/accounting/errors/send_message/1', method='post', data={'message':'abc 123'})

    def test_accounting_import_step0(self):
        self.call('/accounting/main/accounting/import/step/0', status_expected=302)
        url_splited = self.response.url.split('/')
        self.assertEquals('/'.join(url_splited[3:-1]), 'accounting/main/accounting/import/step/1', self.response.url)
        self.assertTrue(match(r'[a-z0-9\-]+', url_splited[-1]), self.response.url)
        session_key = 'T2_ACCOUNTING_IMPORT_{}'.format(url_splited[-1])

    def test_accounting_import_step1(self):
        sess = self.session
        sess.update({'T2_ACCOUNTING_IMPORT_def-123-abc': {'is_valid': True, 'has_data': False}})
        sess.save()
        self.call_check_html('/accounting/main/accounting/import/step/1/def-123-abc', alert_expected='')

    def test_accounting_import_step2(self):
        sess = self.session
        sess.update({'T2_ACCOUNTING_IMPORT_def-123-abc': {'is_valid': True, 'has_data': True, 'year':1, 'data': {'nop':[], 'to_delete':[], 'to_update':[]}}})
        sess.save()
        self.call_check_html('/accounting/main/accounting/import/step/2/def-123-abc', alert_expected='')

    def test_budget_available_list(self):
        self.call_check_json('/accounting/main/budget/available_list'),

    def test_budget_copy(self):
        self.call_check_redirect('/accounting/main/budget/1/copy', redirect_url='/accounting/main/budget/2/edit')

    def test_budget_get_infos(self):
        self.call_check_json('/accounting/main/budget/1/get_infos')

    def test_budget_pdf(self):
        self.call_check_pdf('/accounting/main/budget/1/pdf/')

    def test_accounting_budget_view(self):
        self.call_check_text('/accounting/main/accounting/budget_view', data={'costcenter':1})
