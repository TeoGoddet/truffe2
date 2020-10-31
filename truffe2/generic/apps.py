# -*- coding: utf-8 -*-
'''
apps.py
'''

from django.apps import AppConfig


class GenericConfig(AppConfig):
    name = 'generic'
    verbose_name = "Generic"
    
    def ready(self):
        from generic.models import GenericModel
        GenericModel.startup()
