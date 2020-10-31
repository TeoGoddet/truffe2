# -*- coding: utf-8 -*-

from django.conf.urls import url
from units.views import accreds_list, accreds_list_json, accreds_logs_list, \
    accreds_logs_list_json, accreds_renew, accreds_edit, accreds_delete, \
    accreds_validate, accreds_add, role_userslist

urlpatterns = [
    url(r'^accreds/$', accreds_list, name='units-views-accreds_list', prefix='units.views'),
    url(r'^accreds/json$', accreds_list_json, name='units-views-accreds_list_json', prefix='units.views'),
    url(r'^accreds/logs/$', accreds_logs_list, name='units-views-accreds_logs_list', prefix='units.views'),
    url(r'^accreds/logs/json$', accreds_logs_list_json, name='units-views-accreds_logs_list_json', prefix='units.views'),
    url(r'^accreds/(?P<pk>[0-9,]+)/renew$', accreds_renew, name='units-views-accreds_renew', prefix='units.views'),
    url(r'^accreds/(?P<pk>[0-9~]+)/edit$', accreds_edit, name='units-views-accreds_edit', prefix='units.views'),
    url(r'^accreds/(?P<pk>[0-9,]+)/delete$', accreds_delete, name='units-views-accreds_delete', prefix='units.views'),
    url(r'^accreds/(?P<pk>[0-9,]+)/validate$', accreds_validate, name='units-views-accreds_validate', prefix='units.views'),
    url(r'^accreds/add$', accreds_add, name='units-views-accreds_add', prefix='units.views'),
    url(r'^role/(?P<pk>\d*)/users$', role_userslist, name='units-views-role_userslist', prefix='units.views'),
]
