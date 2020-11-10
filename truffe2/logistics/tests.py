# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from main.test_tools import TruffeTestAbstract


class LogisticsNoLoginTest(TruffeTestAbstract):
    
    def test_room_search(self):
        self.call_check_redirect('/logistics/room/search')

    def test_supply_search(self):
        self.call_check_redirect('/logistics/supply/search')

    def test_loanagreement(self):
        self.call_check_redirect('/logistics/loanagreement/1/pdf/')

    def test_roomreservation_list(self):
        self.call_check_redirect('/logistics/roomreservation/')

    def test_roomreservation_mayi(self):
        self.call_check_redirect('/logistics/roomreservation/mayi')

    def test_roomreservation_json(self):
        self.call_check_redirect('/logistics/roomreservation/json')

    def test_roomreservation_deleted(self):
        self.call_check_redirect('/logistics/roomreservation/deleted')

    def test_roomreservation_logs(self):
        self.call_check_redirect('/logistics/roomreservation/logs')

    def test_roomreservation_logs_json(self):
        self.call_check_redirect('/logistics/roomreservation/logs/json')

    def test_roomreservation_add(self):
        self.call_check_redirect('/logistics/roomreservation/%7E/edit')

    def test_roomreservation_edit(self):
        self.call_check_redirect('/logistics/roomreservation/1/edit')

    def test_roomreservation_delete(self):
        self.call_check_redirect('/logistics/roomreservation/1/delete')

    def test_roomreservation_show(self):
        self.call_check_redirect('/logistics/roomreservation/1/')

    def test_roomreservation_switch_status(self):
        self.call_check_redirect('/logistics/roomreservation/1/switch_status')

    def test_roomreservation_calendar(self):
        self.call_check_redirect('/logistics/roomreservation/calendar/')

    def test_roomreservation_calendar_json(self):
        self.call_check_redirect('/logistics/roomreservation/calendar/json')

    def test_roomreservation_related_calendar(self):
        self.call_check_redirect('/logistics/roomreservation/related/calendar/')

    def test_roomreservation_related_calendar_json(self):
        self.call_check_redirect('/logistics/roomreservation/related/calendar/json')

    def test_roomreservation_related(self):
        self.call_check_redirect('/logistics/roomreservation/related/')

    def test_roomreservation_related_json(self):
        self.call_check_redirect('/logistics/roomreservation/related/json')

    def test_roomreservation_specific_calendar(self):
        self.call_check_redirect('/logistics/roomreservation/specific/1/calendar/')

    def test_roomreservation_specific_calendar_json(self):
        self.call_check_redirect('/logistics/roomreservation/specific/1/calendar/json')

    def test_roomreservation_directory(self):
        self.call_check_redirect('/logistics/roomreservation/directory/')

    def test_roomreservation_contact(self):
        self.call_check_redirect('/logistics/roomreservation/1/contact/creator') 


class LogisticsWithLoginTest(TruffeTestAbstract):
    
    login_username = 'admin'
    
    def test_room_search(self):
        self.call_check_json('/logistics/room/search')
        self.call_check_json('/logistics/room/search', data={'q':'room'})
        self.call_check_json('/logistics/room/search', data={'init':1})
        self.call_check_json('/logistics/room/search', data={'unit_pk':2})

    def test_supply_search(self):
        self.call_check_json('/logistics/supply/search')
        self.call_check_json('/logistics/supply/search', data={'q':'room'})
        self.call_check_json('/logistics/supply/search', data={'init':1})
        self.call_check_json('/logistics/supply/search', data={'unit_pk':2})

    def test_loanagreement(self):
        self.call_check_pdf('/logistics/loanagreement/1/pdf/')

    def test_roomreservation_list(self):
        self.call_check_html('/logistics/roomreservation/')

    def test_roomreservation_mayi(self):
        self.call_check_json('/logistics/roomreservation/mayi')

    def test_roomreservation_json(self):
        self.call_check_json('/logistics/roomreservation/json')

    def test_roomreservation_deleted(self):
        self.call_check_html('/logistics/roomreservation/deleted')

    def test_roomreservation_logs(self):
        self.call_check_html('/logistics/roomreservation/logs')

    def test_roomreservation_logs_json(self):
        self.call_check_json('/logistics/roomreservation/logs/json')

    def test_roomreservation_add(self):
        self.call_check_html('/logistics/roomreservation/~/edit')
        self.call_check_redirect('/logistics/roomreservation/~/edit', method='post',
                                 data={'title':'reserv', 'start_date':'2020-01-01', 'end_date':'2020-12-31', 'reason':'because', 'room':1},
                                 redirect_url='/logistics/roomreservation/2/')

    def test_roomreservation_edit(self):
        self.call_check_html('/logistics/roomreservation/1/edit')
        self.call_check_html('/logistics/roomreservation/1/edit', method='post',
                            data={'title':'reserv', 'start_date':'2030-01-01', 'end_date':'2030-12-31', 'reason':'because', 'room':1})

    def test_roomreservation_delete(self):
        self.call_check_html('/logistics/roomreservation/1/delete')
        self.call_check_redirect('/logistics/roomreservation/1/delete', method='post',
                                 data={'do':'it'}, redirect_url='/logistics/roomreservation/')

    def test_roomreservation_show(self):
        self.call_check_html('/logistics/roomreservation/1/')

    def test_roomreservation_switch_status(self):
        self.call_check_text('/logistics/roomreservation/1/switch_status', data={'dest_status':'2_online', 'from_list':'from_list'})
        self.call_check_text('/logistics/roomreservation/1/switch_status?dest_status=2_online&from_list=from_list', method='post', data={'do':'it'})
        self.assertIn('window.location.reload();', self.response.content.decode('utf-8'))

    def test_roomreservation_calendar(self):
        self.call_check_html('/logistics/roomreservation/calendar/')

    def test_roomreservation_calendar_json(self):
        self.call_check_json('/logistics/roomreservation/calendar/json', data={'upk':1, 'start':1577833200, 'end':1609455599})

    def test_roomreservation_related_calendar(self):
        self.call_check_html('/logistics/roomreservation/related/calendar/')

    def test_roomreservation_related_calendar_json(self):
        self.call_check_json('/logistics/roomreservation/related/calendar/json', data={'upk':1, 'start':1577833200, 'end':1609455599})

    def test_roomreservation_related(self):
        self.call_check_html('/logistics/roomreservation/related/')

    def test_roomreservation_related_json(self):
        self.call_check_json('/logistics/roomreservation/related/json')

    def test_roomreservation_specific_calendar(self):
        self.call_check_html('/logistics/roomreservation/specific/1/calendar/')

    def test_roomreservation_specific_calendar_json(self):
        self.call_check_json('/logistics/roomreservation/specific/1/calendar/json', data={'upk':1, 'start':1577833200, 'end':1609455599})

    def test_roomreservation_directory(self):
        self.call_check_html('/logistics/roomreservation/directory/')

    def test_roomreservation_contact(self):
        self.call_check_html('/logistics/roomreservation/~/edit')
        self.call_check_redirect('/logistics/roomreservation/~/edit', method='post',
                                 data={'title':'reserv', 'start_date':'2020-01-01', 'end_date':'2020-12-31', 'reason':'because', 'room':1},
                                 redirect_url='/logistics/roomreservation/2/')
        
        self.call_check_text('/logistics/roomreservation/2/contact/creator') 
        self.call_check_text('/logistics/roomreservation/2/contact/creator', method='post', data={'key':'creator', 'subject':'ask','message':'blabla', 'receive_copy':True})
