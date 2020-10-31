# -*- coding: utf-8 -*-

from django.conf.urls import url
from generic.views import check_unit_name

urlpatterns = [
    url('check_unit_name', check_unit_name, name='generic-views-check_unit_name', prefix='generic.views'),
]
