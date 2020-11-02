# -*- coding: utf-8 -*-

from django.conf.urls import url
from communication.views import display_search, logo_public_load, \
    logo_public_list, website_news, random_slide, ecrans

urlpatterns = [
    url(r'^ecrans$', ecrans, name='communication-views-ecrans'),
    url(r'^random_slide$', random_slide, name='communication-views-random_slide'),
    url(r'^website_news$', website_news, name='communication-views-website_news'),
    url(r'^logo_public_list$', logo_public_list, name='communication-views-logo_public_list'),
    url(r'^logo_public_load$', logo_public_load, name='communication-views-logo_public_load'),
    url('display/search', display_search, name='communication-views-display_search'),
]
