# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.template.base import TemplateDoesNotExist

from main.test_tools import TruffeTestAbstract


class UsersNoLoginTest(TruffeTestAbstract):
    
    def test_login(self):
        self.call_check_alert('/users/login', alert_expected="")

    def test_login_done(self):
        self.call_check_alert('/users/login_done', alert_expected="")

    def test_login_cptd(self):
        self.call_check_alert('/users/login_cptd', alert_expected="")

    def test_create_external(self):
        self.call_check_redirect('/users/create_external')

    def test_password_change_check(self):
        self.call_check_redirect('/users/password_change_check')

    def test_password_change_done(self):
        self.call_check_redirect('/users/password_change/done/')

    def test_password_reset(self):
        # TODO : problem of template not found 'registration/password_reset_form.html'
        with self.assertRaises(TemplateDoesNotExist) as context:
            self.call_check_alert('/users/password_reset/', alert_expected="")
        self.assertEqual(str(context.exception), 'registration/password_reset_form.html')
        
    def test_reset(self):
        self.call_check_alert('/users/reset/abc123/azertdDESS45-fgsfs54545/', alert_expected="")

    def test_set_body(self):
        self.call_check_redirect('/users/set_body/m')

    def test_users(self):
        self.call_check_redirect('/users/users/')

    def test_users_json(self):
        self.call_check_redirect('/users/users/json')

    def test_users_id(self):
        self.call_check_redirect('/users/users/1')

    def test_users_vcard(self):
        self.call_check_redirect('/users/users/1/vcard')

    def test_users_edit(self):
        self.call_check_redirect('/users/users/1/edit')

    def test_users_profile_picture(self):
        self.call_check_redirect('/users/users/1/profile_picture')

    def test_myunit(self):
        self.call_check_redirect('/users/myunit/')

    def test_myunit_json(self):
        self.call_check_redirect('/users/myunit/json')

    def test_myunit_vcard(self):
        self.call_check_redirect('/users/myunit/vcard')

    def test_myunit_pdf(self):
        self.call_check_redirect('/users/myunit/pdf/')

    def test_ldap_search(self):
        self.call_check_redirect('/users/ldap/search')


class UsersWithLoginTest(TruffeTestAbstract):

    def setUp(self):
        TruffeTestAbstract.setUp(self)
        self.connect_admin()   
    
    def test_login(self):
        self.call('/users/login', status_expected=302)
        self.assertRedirects(self.response, '/')

    def test_login_done(self):
        self.call('/users/login_done', status_expected=302)
        self.assertRedirects(self.response, '/')

    def test_login_cptd(self):
        self.call('/users/login_cptd', status_expected=302)
        self.assertRedirects(self.response, '/')

    def test_create_external(self):
        self.call_check_alert('/users/create_external', alert_expected="")

    def test_password_change_check(self):
        self.call('/users/password_change_check', status_expected=302)
        self.assertRedirects(self.response, '/users/users/1')

    def test_password_change_done(self):
        self.call('/users/password_change/done/', status_expected=302)
        self.assertRedirects(self.response, '/users/users/1')
                
    def test_password_reset(self):
        # TODO : problem of template not found 'registration/password_reset_form.html'
        with self.assertRaises(TemplateDoesNotExist) as context:
            self.call_check_alert('/users/password_reset/', alert_expected="")
        self.assertEqual(str(context.exception), 'registration/password_reset_form.html')
        
    def test_reset(self):
        self.call_check_alert('/users/reset/abc123/azertdDESS45-fgsfs54545/', alert_expected="")

    def test_set_body(self):
        self.call_check_alert('/users/set_body/m', alert_expected="")

    def test_users(self):
        self.call_check_alert('/users/users/', alert_expected="")

    def test_users_json(self):
        self.call_check_alert('/users/users/json', alert_expected="")

    def test_users_id(self):
        self.call_check_alert('/users/users/1', alert_expected="")

    def test_users_vcard(self):
        self.call_check_alert('/users/users/1/vcard', alert_expected="")

    def test_users_edit(self):
        self.call_check_alert('/users/users/1/edit', alert_expected="")

    def test_users_profile_picture(self):
        self.call('/users/users/1/profile_picture', status_expected=302)
        self.assertRedirects(self.response, '/media/cache/users/1.png')

    def test_myunit(self):
        self.call_check_alert('/users/myunit/',
                             alert_expected=u"Malheureusement, tu ne disposes pas des droits nécessaires pour afficher cette liste, dans aucune unité !")                              

    def test_myunit_json(self):
        self.call_check_alert('/users/myunit/json', alert_expected="")

    def test_myunit_vcard(self):
        self.call_check_alert('/users/myunit/vcard', alert_expected="")

    def test_myunit_pdf(self):
        self.call_check_alert('/users/myunit/pdf/', alert_expected="")

    def test_ldap_search(self):
        # TODO : problem to test LDAP
        from _ldap import SERVER_DOWN
        with self.assertRaises(SERVER_DOWN) as context:
            self.call_check_alert('/users/ldap/search', alert_expected="")
        self.assertIn(u"Can't contact LDAP server", str(context.exception))
