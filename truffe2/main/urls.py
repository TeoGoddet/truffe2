# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from main.views import HaystackSearchView, home, \
    get_to_moderate, link_base, \
    last_100_logging_entries, set_homepage, \
    file_download_list, \
    file_download, \
    signabledocument_download, \
    signabledocument_signs, signabledocument_sign

urlpatterns = [
    url(r'^$', home, name='main-views-home', prefix='main.views'),
    url(r'^get_to_moderate$', get_to_moderate, name='main-views-get_to_moderate', prefix='main.views'),

    url(r'^link/base$', link_base, name='main-views-link_base', prefix='main.views'),
    url(r'^last_100_logging_entries$', last_100_logging_entries, name='main-views-last_100_logging_entries', prefix='main.views'),

    url(r'^search/?$', login_required(HaystackSearchView()), name='search_view', prefix='main.views'),

    url(r'^set_homepage$', set_homepage, name='main-views-set_homepage', prefix='main.views'),

    url(r'^file/download_list/$', file_download_list, name='main-views-file_download_list', prefix='main.views'),
    url(r'^file/download/(?P<pk>[0-9,]+)$', file_download, name='main-views-file_download', prefix='main.views'),

    url(r'^signabledocument/download/(?P<pk>[0-9,]+)$', signabledocument_download, name='main-views-signabledocument_download', prefix='main.views'),
    url(r'^signabledocument/sign/(?P<pk>[0-9,]+)$', signabledocument_sign, name='main-views-signabledocument_sign', prefix='main.views'),
    url(r'^signabledocument/signs/$', signabledocument_signs, name='main-views-signabledocument_signs', prefix='main.views'),
]
