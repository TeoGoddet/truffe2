# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract
from os.path import join, dirname


class AccountingToolsNoLoginTest(TruffeTestAbstract):
    
    def test_subvention_export(self):
        self.call_check_redirect('/accounting/tools/subvention/1/export')

    def test_subvention_export_all(self):
        self.call_check_redirect('/accounting/tools/subvention/export_all')

    def test_invoice_pdf(self):
        self.call_check_redirect('/accounting/tools/invoice/1/pdf/')

    def test_invoice_bvr(self):
        self.call_check_redirect('/accounting/tools/invoice/1/bvr/')

    def test_withdrawal_pdf(self):
        self.call_check_redirect('/accounting/tools/withdrawal/1/pdf/')

    def test_withdrawal_list(self):
        self.call_check_redirect('/accounting/tools/withdrawal/list/')

    def test_withdrawal_infos(self):
        self.call_check_redirect('/accounting/tools/withdrawal/1/infos/')

    def test_internaltransfer_pdf(self):
        self.call_check_redirect('/accounting/tools/internaltransfer/1/pdf/')

    def test_expenseclaim_pdf(self):
        self.call_check_redirect('/accounting/tools/expenseclaim/1/pdf/')

    def test_cashbook_pdf(self):
        self.call_check_redirect('/accounting/tools/cashbook/1/pdf/')

    def test_financialprovider_list(self):
        self.call_check_redirect('/accounting/tools/financialprovider/list/')

    def test_providerinvoice_pdf(self):
        self.call_check_redirect('/accounting/tools/providerinvoice/1/pdf/')

    def test_internaltransfer_csv(self):
        self.call_check_redirect('/accounting/tools/internaltransfer/1/csv/')

    def test_expenseclaim_csv(self):
        self.call_check_redirect('/accounting/tools/expenseclaim/1/csv/')

    def test_cashbook_csv(self):
        self.call_check_redirect('/accounting/tools/cashbook/1/csv/')

    def test_subventionfile_upload(self):
        self.call_check_redirect('/accounting/tools/subventionfile/upload')

    def test_subventionfile_delete(self):
        self.call_check_redirect('/accounting/tools/subventionfile/1/delete')

    def test_subventionfile_get(self):
        self.call_check_redirect('/accounting/tools/subventionfile/1/get/')

    def test_subventionfile_thumbnail(self):
        self.call_check_redirect('/accounting/tools/subventionfile/1/thumbnail') 


class AccountingToolsWithLoginTest(TruffeTestAbstract):
    
    def test_subvention_export(self):
        self.call_check_pdf('/accounting/tools/subvention/1/export')

    def test_subvention_export_all(self):
        self.call_check_pdf('/accounting/tools/subvention/export_all')

    def test_invoice_pdf(self):
        self.call_check_pdf('/accounting/tools/invoice/1/pdf/')

    def test_invoice_bvr(self):
        self.call_check_text('/accounting/tools/invoice/1/bvr/')

    def test_withdrawal_pdf(self):
        self.call_check_pdf('/accounting/tools/withdrawal/1/pdf/')

    def test_withdrawal_list(self):
        self.call_check_json('/accounting/tools/withdrawal/list/', data={'upk':1, 'ypk':1})

    def test_withdrawal_infos(self):
        self.call_check_json('/accounting/tools/withdrawal/1/infos/')

    def test_internaltransfer_pdf(self):
        self.call_check_pdf('/accounting/tools/internaltransfer/1/pdf/')

    def test_expenseclaim_pdf(self):
        self.call_check_pdf('/accounting/tools/expenseclaim/1/pdf/')

    def test_cashbook_pdf(self):
        self.call_check_pdf('/accounting/tools/cashbook/1/pdf/')

    def test_financialprovider_list(self):
        self.call_check_json('/accounting/tools/financialprovider/list/')

    def test_providerinvoice_pdf(self):
        self.call_check_pdf('/accounting/tools/providerinvoice/1/pdf/')

    def test_internaltransfer_csv(self):
        self.call_check_text('/accounting/tools/internaltransfer/1/csv/')

    def test_expenseclaim_csv(self):
        self.call_check_text('/accounting/tools/expenseclaim/1/csv/')

    def test_cashbook_csv(self):
        self.call_check_text('/accounting/tools/cashbook/1/csv/')

    def test_subventionfile_upload(self):
        sess = self.session
        sess.update({'pca_files_abc': []})
        sess.save()
        with open(join(dirname(dirname(__file__)), 'media', 'uploads', 'files', 'bigbox.mp3'), 'rb') as file_upload:
            self.call_check_json('/accounting/tools/subventionfile/upload?key=abc', data={'files[]':file_upload}, method="post")

    def test_subventionfile_delete(self):
        sess = self.session
        sess.update({'pca_files_abc': [1]})
        sess.save()
        self.call_check_text('/accounting/tools/subventionfile/1/delete?key=abc')

    def test_subventionfile_get(self):
        self.call_check_text('/accounting/tools/subventionfile/1/get/', data={'down':1})

    def test_subventionfile_thumbnail(self):
        self.call_check_text('/accounting/tools/subventionfile/1/thumbnail') 
