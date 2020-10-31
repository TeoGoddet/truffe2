
# -*- coding: utf-8 -*-

from django.conf.urls import url
from vehicles.views import booking_pdf

urlpatterns = [
    url(r'^booking/(?P<pk>[0-9]+)/pdf/', booking_pdf, name='vehicles-views-booking_pdf', prefix='vehicles.views'),
]
