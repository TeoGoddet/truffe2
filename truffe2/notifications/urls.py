# -*- coding: utf-8 -*-

from django.conf.urls import url
from notifications.views import mark_as_read, \
    notification_restrictions_update, \
    dropdown, goto, \
    notification_center, \
    notification_keys, \
    notification_json, \
    notification_restrictions

urlpatterns = [
    url(r'^dropdown$', dropdown, name='notifications-views-dropdown'),
    url(r'^goto/(?P<pk>[0-9]+)$', goto, name='notifications-views-goto'),
    url(r'^center/$', notification_center, name='notifications-views-notification_center'),
    url(r'^center/keys$', notification_keys, name='notifications-views-notification_keys'),
    url(r'^center/json$', notification_json, name='notifications-views-notification_json'),
    url(r'^center/restrictions$', notification_restrictions, name='notifications-views-notification_restrictions'),
    url(r'^center/restrictions/update$', notification_restrictions_update, name='notifications-views-notification_restrictions_update'),
    url(r'^read$', mark_as_read, name='notifications-views-mark_as_read'),
]
