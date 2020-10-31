# -*- coding: utf-8 -*-

from django.conf.urls import url
from accounting_tools.views import cashbook_csv, expenseclaim_csv, \
    internaltransfer_csv, provider_invoice_pdf, export_demands_yearly, \
    export_all_demands, provider_available_list, \
    cashbook_pdf, expenseclaim_pdf, internaltransfer_pdf, get_withdrawal_infos, \
    withdrawal_available_list, withdrawal_pdf, invoice_bvr, invoice_pdf

urlpatterns = [
    url(r'^subvention/(?P<ypk>[0-9]+)/export$', export_demands_yearly, name='accounting_tools-views-export_demands_yearly', prefix='accounting_tools.views'),
    url(r'^subvention/export_all$', export_all_demands, name='accounting_tools-views-export_all_demands', prefix='accounting_tools.views'),

    url(r'^invoice/(?P<pk>[0-9]+)/pdf/', invoice_pdf, name='accounting_tools-views-invoice_pdf', prefix='accounting_tools.views'),
    url(r'^invoice/(?P<pk>[0-9]+)/bvr/', invoice_bvr, name='accounting_tools-views-invoice_bvr', prefix='accounting_tools.views'),

    url(r'^withdrawal/(?P<pk>[0-9]+)/pdf/', withdrawal_pdf, name='accounting_tools-views-withdrawal_pdf', prefix='accounting_tools.views'),
    url(r'^withdrawal/list/', withdrawal_available_list, name='accounting_tools-views-withdrawal_available_list', prefix='accounting_tools.views'),
    url(r'^withdrawal/(?P<pk>[0-9]+)/infos/', get_withdrawal_infos, name='accounting_tools-views-get_withdrawal_infos', prefix='accounting_tools.views'),

    url(r'^internaltransfer/(?P<pk>[0-9,]+)/pdf/', internaltransfer_pdf, name='accounting_tools-views-internaltransfer_pdf', prefix='accounting_tools.views'),
    url(r'^expenseclaim/(?P<pk>[0-9]+)/pdf/', expenseclaim_pdf, name='accounting_tools-views-expenseclaim_pdf', prefix='accounting_tools.views'),
    url(r'^cashbook/(?P<pk>[0-9]+)/pdf/', cashbook_pdf, name='accounting_tools-views-cashbook_pdf', prefix='accounting_tools.views'),

    url(r'^financialprovider/list/', provider_available_list, name='accounting_tools-views-provider_available_list', prefix='accounting_tools.views'),
    url(r'^providerinvoice/(?P<pk>[0-9]+)/pdf/', provider_invoice_pdf, name='accounting_tools-views-provider_invoice_pdf', prefix='accounting_tools.views'),
    
    url(r'^internaltransfer/(?P<pk>[0-9,]+)/csv/', internaltransfer_csv, name='accounting_tools-views-internaltransfer_csv', prefix='accounting_tools.views'),
    url(r'^expenseclaim/(?P<pk>[0-9,]+)/csv/', expenseclaim_csv, name='accounting_tools-views-expenseclaim_csv', prefix='accounting_tools.views'),
    url(r'^cashbook/(?P<pk>[0-9,]+)/csv/', cashbook_csv, name='accounting_tools-views-cashbook_csv', prefix='accounting_tools.views'),
]
