# -*- coding: utf-8 -*-
'''
Unit test tools for truffe

'''
from bs4 import BeautifulSoup
from json import loads

from django.test import TestCase, Client
from django.test.client import MULTIPART_CONTENT

from main.test_data import initial_data


class TruffeTestAbstract(TestCase, Client):

    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        Client.__init__(self)

    def setUp(self):
        TestCase.setUp(self)
        initial_data()
        class_name = self.__class__.__name__
        if 'WithLogin' in class_name:
            self.connect_to('admin')
        elif 'WithLog' in class_name:
            user_num = int(class_name[class_name.index('WithLog') + 7])
            self.connect_to('user%d' % user_num)

    def connect_to(self, username):
        self.call_check_html('/users/login', alert_expected='')
        csr_token_input = self.content.findAll('input', {'name': 'csrfmiddlewaretoken'})[0]           
        self.call('/users/login', {'username': username, 'password': username, 'csrfmiddlewaretoken': csr_token_input}, 'post', status_expected=302)

    def _get_default_content_type(self):
        if self.response.status_code != 200:
            return ""
        if '<!DOCTYPE html>' in self.response.content:
            default_type = 'text/html'
        elif len(self.response.content) == 0:
            default_type = 'text/text'
        elif self.response.content.strip()[0] in ('[', '{'):
            default_type = 'application/json'
        elif self.response.content[1:4] == 'PDF':
            default_type = 'application/pdf'
        else:
            default_type = 'text/text'
        return default_type

    def call(self, path, data={}, method='get', status_expected=200):
        self.response = getattr(self, method.lower(), self.get)(path, data, content_type=MULTIPART_CONTENT)
        self.content_type = getattr(self.response, 'content_type', self._get_default_content_type())
        self.content = self.response.content
        if status_expected != 0:
            self.assertEqual(self.response.status_code, status_expected, "HTTP error [%s]:%s" % (self.response.status_code, self.get_div('text-center error-box')))

    def call_check_redirect(self, path, data={}, method='get', redirect_url=None):
        self.call(path, data, method, status_expected=302)
        self.assertRedirects(self.response, '/users/login?next=%s' % path if redirect_url is None else redirect_url)        

    def call_check_html(self, path, data={}, method='get', alert_expected=''):
        self.call(path, data, method)
        try:
            self.content = BeautifulSoup(self.response.content, "html.parser")
        except Exception:
            self.content = self.response.content
        self.assertEqual(self.content_type, "text/html")
        alert_dom = self.get_div('alert alert-danger')
        self.assertEqual(alert_dom, alert_expected)

    def call_check_json(self, path, data={}, method='get'):
        self.call(path, data, method)
        self.assertEqual(self.content_type, "application/json")
        self.content = loads(self.response.content)

    def call_check_pdf(self, path, data={}, method='get'):
        self.call(path, data, method)
        self.assertEqual(self.content_type, "application/pdf")

    def call_check_text(self, path, data={}, method='get'):
        self.call(path, data, method)
        self.assertEqual(self.content_type, "text/text")

    def get_div(self, class_to_find):
        try:
            div_dom = self.content.findAll('div', {'class': class_to_find})
            return "\n".join([item.text.strip() for item in div_dom])
        except Exception:
            return None
