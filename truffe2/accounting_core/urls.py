# -*- coding: utf-8 -*-

from django.conf.urls import url
from accounting_core.views import copy_accounting_year, pdf_list_cost_centers, \
    pdf_list_accounts, leaves_cat_by_year, parents_cat_by_year, accounts_by_year, \
    costcenter_available_list, account_available_list, tva_available_list, \
    users_available_list_by_unit

urlpatterns = [
    url(r'^accountingyear/(?P<pk>[0-9,]+)/copy$', copy_accounting_year, name='accounting_core-views-copy_accounting_year', prefix='accounting_core.views'),
    url(r'^accountingyear/(?P<pk>[0-9]+)/cost_centers$', pdf_list_cost_centers, name='accounting_core-views-pdf_list_cost_centers', prefix='accounting_core.views'),
    url(r'^accountingyear/(?P<pk>[0-9]+)/accounts$', pdf_list_accounts, name='accounting_core-views-pdf_list_accounts', prefix='accounting_core.views'),
    url(r'^accountingyear/(?P<ypk>[0-9]+)/get_leaves_cat$', leaves_cat_by_year, name='accounting_core-views-leaves_cat_by_year', prefix='accounting_core.views'),
    url(r'^accountingyear/(?P<ypk>[0-9]+)/get_parents_cat$', parents_cat_by_year, name='accounting_core-views-parents_cat_by_year', prefix='accounting_core.views'),
    url(r'^accountingyear/(?P<ypk>[0-9]+)/get_accounts$', accounts_by_year, name='accounting_core-views-accounts_by_year', prefix='accounting_core.views'),

    url(r'^costcenter/available_list$', costcenter_available_list, name='accounting_core-views-costcenter_available_list', prefix='accounting_core.views'),
    url(r'^account/available_list$', account_available_list, name='accounting_core-views-account_available_list', prefix='accounting_core.views'),
    url(r'^tva/available_list$', tva_available_list, name='accounting_core-views-tva_available_list', prefix='accounting_core.views'),
    url(r'^unit/(?P<upk>[0-9]+)/users_available_list$', users_available_list_by_unit, name='accounting_core-views-users_available_list_by_unit', prefix='accounting_core.views'),
]
