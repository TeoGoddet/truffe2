# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from main.test_tools import TruffeTestAbstract
from main.test_data import datetime_aware


class VehiculesNoLoginTest(TruffeTestAbstract):
    
    def test_booking_pdf(self):
        self.call_check_redirect('/vehicles/booking/1/pdf/')

    def test_booking_list(self):
        self.call_check_redirect('/vehicles/booking/')

    def test_booking_mayi(self):
        self.call_check_redirect('/vehicles/booking/mayi')

    def test_booking_json(self):
        self.call_check_redirect('/vehicles/booking/json')

    def test_booking_deleted(self):
        self.call_check_redirect('/vehicles/booking/deleted')

    def test_booking_logs(self):
        self.call_check_redirect('/vehicles/booking/logs')

    def test_booking_logs_json(self):
        self.call_check_redirect('/vehicles/booking/logs/json')

    def test_booking_edit(self):
        self.call_check_redirect('/vehicles/booking/1/edit')

    def test_booking_delete(self):
        self.call_check_redirect('/vehicles/booking/1/delete')

    def test_booking_show(self):
        self.call_check_redirect('/vehicles/booking/1/')

    def test_booking_switch_status(self):
        self.call_check_redirect('/vehicles/booking/1/switch_status')

    def test_booking_calendar(self):
        self.call_check_redirect('/vehicles/booking/calendar/')

    def test_booking_calendar_json(self):
        self.call_check_redirect('/vehicles/booking/calendar/json')

    def test_booking_related_calendar(self):
        self.call_check_redirect('/vehicles/booking/related/calendar/')

    def test_booking_related_calendar_json(self):
        self.call_check_redirect('/vehicles/booking/related/calendar/json')

    def test_booking_contact(self):
        self.call_check_redirect('/vehicles/booking/1/contact/canedit')


class VehiculesWithLoginTest(TruffeTestAbstract):
    
    login_username = 'admin'
    
    def test_booking_pdf(self):
        self.call_check_pdf('/vehicles/booking/1/pdf/')

    def test_booking_list(self):
        self.call_check_html('/vehicles/booking/')

    def test_booking_mayi(self):
        self.call_check_json('/vehicles/booking/mayi')

    def test_booking_json(self):
        self.call_check_json('/vehicles/booking/json', data={'upk':1})

    def test_booking_deleted(self):
        from vehicles.models import Booking
        Booking(id=2, unit_id=1, title="bad booking", responsible_id=1, reason="why not?", provider_id=1,
                vehicletype_id=1, card_id=1, location_id=1, start_date=datetime_aware(2000, 1, 1), end_date=datetime_aware(2099, 12, 31), deleted=True).save()
        self.call_check_html('/vehicles/booking/deleted', data={'upk':1})
        self.call_check_redirect('/vehicles/booking/deleted', method='post', data={'upk':1, 'pk':2}, redirect_url='/vehicles/booking/')

    def test_booking_logs(self):
        self.call_check_html('/vehicles/booking/logs')

    def test_booking_logs_json(self):
        self.call_check_json('/vehicles/booking/logs/json')

    def test_booking_add(self):
        self.call_check_html('/vehicles/booking/~/edit')
        self.call_check_redirect('/vehicles/booking/~/edit', method='post', redirect_url='/vehicles/booking/2/',
                                 data={'unit':1, 'title':"booking", 'responsible':1, 'reason':"why not?",
                                       'start_date':'2020-01-01 00:00:00', 'end_date':'2020-12-31 23:59:59',
                                       'provider':1, 'vehicletype':1, 'card':1, 'location':1})

    def test_booking_edit(self):
        self.call_check_html('/vehicles/booking/1/edit')
        self.call_check_redirect('/vehicles/booking/1/edit', method='post', redirect_url='/vehicles/booking/1/',
                                 data={'unit':1, 'title':"booking", 'responsible': 1, 'reason':"why not?",
                                       'start_date':'2020-01-01 00:00:00', 'end_date':'2020-12-31 23:59:59',
                                       'provider':1, 'vehicletype':1, 'card':1, 'location':1})

    def test_booking_delete(self):
        self.call_check_html('/vehicles/booking/1/delete')
        self.call_check_redirect('/vehicles/booking/1/delete', method='post', data={'do':'it'}, redirect_url='/vehicles/booking/')

    def test_booking_show(self):
        self.call_check_html('/vehicles/booking/1/')

    def test_booking_switch_status(self):
        self.call_check_text('/vehicles/booking/1/switch_status', data={'dest_status':'2_online', 'from_list':'from_list'})
        self.call_check_text('/vehicles/booking/1/switch_status?dest_status=2_online&from_list=from_list', method='post', data={'do':'it'})
        self.assertIn('window.location.reload();', self.response.content.decode('utf-8'))
        
    def test_booking_calendar(self):
        self.call_check_html('/vehicles/booking/calendar/')

    def test_booking_calendar_json(self):
        self.call_check_json('/vehicles/booking/calendar/json', data={'upk':1, 'start':1577833200, 'end':1609455599})

    def test_booking_related_calendar(self):
        self.call_check_html('/vehicles/booking/related/calendar/')

    def test_booking_related_calendar_json(self):
        self.call_check_json('/vehicles/booking/related/calendar/json', data={'upk':1, 'start':1577833200, 'end':1609455599})

    def test_booking_contact(self):
        self.call_check_text('/vehicles/booking/1/contact/canedit')
        self.call_check_text('/vehicles/booking/1/contact/canedit', method='post', data={'key':'canedit', 'subject':'ask', 'message':'blabla', 'receive_copy':True})
