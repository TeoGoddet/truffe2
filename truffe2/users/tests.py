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
        self.call_check_html('/users/login')

    def test_login_done(self):
        self.call_check_html('/users/login_done')

    def test_login_cptd(self):
        self.call_check_html('/users/login_cptd')

    def test_create_external(self):
        self.call_check_redirect('/users/create_external')

    def test_password_change_check(self):
        self.call_check_redirect('/users/password_change_check')

    def test_password_change_done(self):
        self.call_check_redirect('/users/password_change/done/')

    def test_password_reset(self):
        # TODO : problem of template not found 'registration/password_reset_form.html'
        with self.assertRaises(TemplateDoesNotExist) as context:
            self.call_check_html('/users/password_reset/')
        self.assertEqual(str(context.exception), 'registration/password_reset_form.html')
        
    def test_reset(self):
        self.call_check_html('/users/reset/abc123/azertdDESS45-fgsfs54545/')

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
    
    login_username = 'admin'
    
    def test_login(self):
        self.call_check_redirect('/users/login', redirect_url='/')

    def test_login_done(self):
        self.call_check_redirect('/users/login_done', redirect_url='/')

    def test_login_cptd(self):
        self.call_check_redirect('/users/login_cptd', redirect_url='/')

    def test_create_external(self):
        self.call_check_html('/users/create_external')
        self.call_check_redirect('/users/create_external', data={'email':'charles.attand@zmail.com', 'first_name':'Charles', 'last_name':'attand'},
                              method='post', redirect_url='/users/users/')

    def test_password_change_check(self):
        self.call_check_redirect('/users/password_change_check', redirect_url='/users/users/1')

    def test_password_change_done(self):
        self.call_check_redirect('/users/password_change/done/', redirect_url='/users/users/1')
                
    def test_password_reset(self):
        # TODO : problem of template not found 'registration/password_reset_form.html'
        with self.assertRaises(TemplateDoesNotExist) as context:
            self.call_check_html('/users/password_reset/')
        self.assertEqual(str(context.exception), 'registration/password_reset_form.html')
        
    def test_reset(self):
        self.call_check_html('/users/reset/abc123/azertdDESS45-fgsfs54545/')

    def test_set_body(self):
        self.call_check_text('/users/set_body/m')

    def test_users(self):
        self.call_check_html('/users/users/')

    def test_users_json(self):
        self.call_check_json('/users/users/json')

    def test_users_id(self):
        self.call_check_html('/users/users/1')

    def test_users_vcard(self):
        self.call_check_text('/users/users/1/vcard')

    def test_users_edit(self):
        self.call_check_html('/users/users/1/edit')
        
        self.call_check_redirect('/users/users/1/edit', method='post',
                              data={'is_superuser':False, 'username':'admin', 'first_name':'admin', 'last_name':'admin', 'email':'admin@green.ch',
                                    'priv_val_mobile': '0123456789', 'priv_val_email_perso': 'admin@green.ch',
                                    'priv_val_iban_ou_ccp': 'ABCD1234', 'priv_val_adresse': 'aaa', 'priv_val_nom_banque': 'aaa'},
                              redirect_url='/users/users/1')

    def test_users_profile_picture(self):
        self.call_check_redirect('/users/users/1/profile_picture', redirect_url='/media/cache/users/1.png')

    def test_myunit(self):
        self.call_check_html('/users/myunit/')                              

    def test_myunit_json(self):
        self.call_check_json('/users/myunit/json')

    def test_myunit_vcard(self):
        self.call_check_text('/users/myunit/vcard')

    def test_myunit_pdf(self):
        self.call_check_pdf('/users/myunit/pdf/')

    def test_ldap_search(self):
        # TODO : problem to test LDAP
        from _ldap import SERVER_DOWN
        with self.assertRaises(SERVER_DOWN) as context:
            self.call_check_html('/users/ldap/search')
        self.assertIn(u"Can't contact LDAP server", str(context.exception))
