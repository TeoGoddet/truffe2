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
    url(r'^dropdown$', dropdown, name='notifications-views-dropdown', prefix='notifications.views'),
    url(r'^goto/(?P<pk>[0-9]+)$', goto, name='notifications-views-goto', prefix='notifications.views'),
    url(r'^center/$', notification_center, name='notifications-views-notification_center', prefix='notifications.views'),
    url(r'^center/keys$', notification_keys, name='notifications-views-notification_keys', prefix='notifications.views'),
    url(r'^center/json$', notification_json, name='notifications-views-notification_json', prefix='notifications.views'),
    url(r'^center/restrictions$', notification_restrictions, name='notifications-views-notification_restrictions', prefix='notifications.views'),
    url(r'^center/restrictions/update$', notification_restrictions_update, name='notifications-views-notification_restrictions_update', prefix='notifications.views'),
    url(r'^read$', mark_as_read, name='notifications-views-mark_as_read', prefix='notifications.views'),
]
