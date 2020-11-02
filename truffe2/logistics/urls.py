# -*- coding: utf-8 -*-

from django.conf.urls import url
from logistics.views import loanagreement_pdf, supply_search, room_search

urlpatterns = [
     url('room/search', room_search, name='logistics-views-room_search'),
    url('supply/search', supply_search, name='logistics-views-supply_search'),
    url(r'^loanagreement/(?P<pk>[0-9]+)/pdf/', loanagreement_pdf, name='logistics-views-loanagreement_pdf'),
]
