# -*- coding: utf-8 -*-

from django.conf.urls import url
from members.views import membership_toggle_fees, membership_delete, \
    memberset_api, memberset_info_api, membership_add, membership_list_json, \
    import_members, export_members, import_members_list

urlpatterns = [
    url(r'^memberset/(?P<pk>[0-9]+)/export$', export_members, name='members-views-export_members'),
    url(r'^memberset/(?P<pk>[0-9]+)/import$', import_members, name='members-views-import_members'),
    url(r'^memberset/(?P<pk>[0-9]+)/import_list$', import_members_list, name='members-views-import_members_list'),
    url(r'^memberset/(?P<pk>[0-9]+)/json$', membership_list_json, name='members-views-membership_list_json'),
    url(r'^memberset/(?P<pk>[0-9]+)/add$', membership_add, name='members-views-membership_add'),

    url(r'^memberset/(?P<pk>[0-9]+)/api/v1/info$', memberset_info_api, name='members-views-memberset_info_api'),
    url(r'^memberset/(?P<pk>[0-9]+)/api/v1/$', memberset_api, name='members-views-memberset_api'),

    url(r'^membership/(?P<pk>[0-9]+)/delete$', membership_delete, name='members-views-membership_delete'),
    url(r'^membership/(?P<pk>[0-9~]+)/toggle_fees$', membership_toggle_fees, name='members-views-membership_toggle_fees'),
]
