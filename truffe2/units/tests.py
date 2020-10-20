# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract, TruffeCmdTestAbstract
from django.conf import settings


class UnitsNoLoginTest(TruffeTestAbstract):
    
    def test_accreds(self):
        self.call_check_redirect('/units/accreds/')

    def test_accreds_json(self):
        self.call_check_redirect('/units/accreds/json')

    def test_accreds_logs(self):
        self.call_check_redirect('/units/accreds/logs/')

    def test_accreds_logs_json(self):
        self.call_check_redirect('/units/accreds/logs/json')

    def test_accreds_renew(self):
        self.call_check_redirect('/units/accreds/1/renew')

    def test_accreds_edit(self):
        self.call_check_redirect('/units/accreds/1/edit')

    def test_accreds_delete(self):
        self.call_check_redirect('/units/accreds/1/delete')

    def test_accreds_validate(self):
        self.call_check_redirect('/units/accreds/1/validate')

    def test_accreds_add(self):
        self.call_check_redirect('/units/accreds/add')

    def test_role_users(self):
        self.call_check_redirect('/units/role/1/users')

    def test_unit(self):
        self.call_check_redirect('/units/unit/')

    def test_unit_mayi(self):
        self.call_check_redirect('/units/unit/mayi')

    def test_unit_json(self):
        self.call_check_redirect('/units/unit/json')

    def test_unit_deleted(self):
        self.call_check_redirect('/units/unit/deleted')

    def test_unit_logs(self):
        self.call_check_redirect('/units/unit/logs')

    def test_unit_logs_json(self):
        self.call_check_redirect('/units/unit/logs/json')

    def test_unit_edit(self):
        self.call_check_redirect('/units/unit/2/edit')

    def test_unit_delete(self):
        self.call_check_redirect('/units/unit/2/delete')

    def test_unit_show(self):
        self.call_check_redirect('/units/unit/2/')


class UnitsWithLoginTest(TruffeTestAbstract):
        
    def test_accreds(self):
        self.call_check_html('/units/accreds/')

    def test_accreds_json(self):
        self.call_check_json('/units/accreds/json')

    def test_accreds_logs(self):
        self.call_check_html('/units/accreds/logs/')

    def test_accreds_logs_json(self):
        self.call_check_json('/units/accreds/logs/json')

    def test_accreds_renew(self):
        self.call_check_html('/units/accreds/1/renew')        
        self.call_check_redirect('/units/accreds/1/renew', method='post', redirect_url='/units/accreds/')

    def test_accreds_edit(self):
        self.call_check_text('/units/accreds/1/edit')
        self.call_check_text('/units/accreds/1/edit', method='post',
                             data={'unit':1, 'role':1, 'display_name':'new', 'no_epfl_sync':False, 'hidden_in_epfl':False, 'hidden_in_truffe':False})
        self.assertIn('window.location.reload();', self.response.content)

    def test_accreds_delete(self):
        self.call_check_html('/units/accreds/1/delete')
        self.call_check_redirect('/units/accreds/1/delete', method='post', redirect_url='/units/accreds/')

    def test_accreds_validate(self):
        self.call_check_html('/units/accreds/2/validate')
        self.call_check_redirect('/units/accreds/2/validate', method='post', redirect_url='/units/accreds/')

    def test_accreds_add(self):
        self.call_check_text('/units/accreds/add')
        self.call_check_text('/units/accreds/add', method='post',
                             data={'unit':1, 'role':1, 'display_name':'new', 'no_epfl_sync':False, 'hidden_in_epfl':False, 'hidden_in_truffe':False, 'user':'admin'})
        self.assertIn('window.location.reload();', self.response.content)

    def test_role_users(self):
        self.call_check_html('/units/role/1/users')

    def test_unit(self):
        self.call_check_html('/units/unit/')

    def test_unit_mayi(self):
        self.call_check_json('/units/unit/mayi')

    def test_unit_json(self):
        self.call_check_json('/units/unit/json')

    def test_unit_deleted(self):
        from units.models import Unit
        Unit(id=3, name='other unit', description='bad unit', is_commission=True, is_equipe=True, deleted=True).save()
        self.call_check_html('/units/unit/deleted')
        self.call_check_redirect('/units/unit/deleted', method='post', data={'pk':3}, redirect_url='/units/unit/')

    def test_unit_logs(self):
        self.call_check_html('/units/unit/logs')

    def test_unit_logs_json(self):
        self.call_check_json('/units/unit/logs/json')

    def test_unit_edit(self):
        self.call_check_html('/units/unit/2/edit')
        self.call_check_redirect('/units/unit/2/edit', method='post', redirect_url='/units/unit/2/',
                                 data={'name':'super unit', 'id_epfl':'blabla', 'description':'mega super unit', 'url':'http://superunit.net',
                                       'is_commission':True, 'is_equipe':True, 'is_hidden':False, 'parent_hierarchique':''})

    def test_unit_delete(self):
        from units.models import Unit
        Unit(id=3, name='other unit', description='bad unit', is_commission=True, is_equipe=True).save()
        self.call_check_html('/units/unit/3/delete')
        self.call_check_redirect('/units/unit/3/delete', method='post', data={'do':'it'}, redirect_url='/units/unit/')

    def test_unit_show(self):
        self.call_check_html('/units/unit/2/')


class UnitsCommandsTest(TruffeCmdTestAbstract):
    
    def test_cron_accreds(self):
        self.call_command()
        
    def test_sync_dit(self):
        self.call_command()
        
    def test_sync_rlc(self):
        from units.models import Unit, Role
        Unit(pk=settings.AUTO_RLC_UNIT_PK, name='RLC', description='RLC').save()
        Role(pk=settings.AUTO_RLC_GIVEN_ROLE, name="RLC", order=1, need_validation=False).save()        
        self.call_command()
    
