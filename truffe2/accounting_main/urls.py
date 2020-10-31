# -*- coding: utf-8 -*-

from django.conf.urls import url
from accounting_main.views import accounting_budget_view, budget_pdf, \
    budget_getinfos, copy_budget, budget_available_list, accounting_import_step2, \
    accounting_import_step1, accounting_import_step0, errors_send_message, \
    accounting_graph

urlpatterns = [
    url(r'^accounting/graph/$', accounting_graph, name='accounting_main-views-accounting_graph', prefix='accounting_main.views'),
    url(r'^accounting/errors/send_message/(?P<pk>[0-9]+)$', errors_send_message, name='accounting_main-views-errors_send_message', prefix='accounting_main.views'),

    url(r'^accounting/import/step/0$', accounting_import_step0, name='accounting_main-views-accounting_import_step0', prefix='accounting_main.views'),
    url(r'^accounting/import/step/1/(?P<key>[0-9\-a-f]+)$', accounting_import_step1, name='accounting_main-views-accounting_import_step1', prefix='accounting_main.views'),
    url(r'^accounting/import/step/2/(?P<key>[0-9\-a-f]+)$', accounting_import_step2, name='accounting_main-views-accounting_import_step2', prefix='accounting_main.views'),

    url(r'^budget/available_list', budget_available_list, name='accounting_main-views-budget_available_list', prefix='accounting_main.views'),
    url(r'^budget/(?P<pk>[0-9]+)/copy$', copy_budget, name='accounting_main-views-copy_budget', prefix='accounting_main.views'),
    url(r'^budget/(?P<pk>[0-9]+)/get_infos$', budget_getinfos, name='accounting_main-views-budget_getinfos', prefix='accounting_main.views'),
    url(r'^budget/(?P<pk>[0-9]+)/pdf/', budget_pdf, name='accounting_main-views-budget_pdf', prefix='accounting_main.views'),

    url(r'^accounting/budget_view', accounting_budget_view, name='accounting_main-views-accounting_budget_view', prefix='accounting_main.views'),
]
