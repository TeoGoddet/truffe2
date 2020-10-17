# -*- coding: utf-8 -*-
'''
Unit test tools for truffe

'''
from bs4 import BeautifulSoup
from south.utils.datetime_utils import datetime

from django.conf import settings
from django.test import TestCase, Client
from django.test.client import MULTIPART_CONTENT

from users.models import TruffeUser


def initial_users_units():
    from units.models import Unit, Role, Accreditation
    admin_user = TruffeUser.objects.create_superuser(username='admin', password='admin', first_name='admin', last_name='admin')
    admin_user.mobile = "0123456789"
    admin_user.adresse = "rue machin"
    admin_user.nom_banque = "Postfinance"
    admin_user.iban_ou_ccp = "0009876543210"
    admin_user.save()
    Role(id=1, name="role", order=1, need_validation=True).save()
    Accreditation(unit=Unit.objects.get(pk=settings.ROOT_UNIT_PK), user=admin_user, role_id=1, need_validation=True).save()
    return admin_user


def initial_main(admin_user):
    from main.models import File, SignableDocument, Signature
    File(id=1, title='title', description='descripption', file='sound/bigbox.mp3', access='all', group='misc').save()
    SignableDocument(id=1, title='unsigned', description='description', file='sound/messagebox.mp3', active=True).save()
    SignableDocument(id=2, title='signed', description='description', file='sound/smallbox.mp3', active=True).save()
    Signature(user=admin_user, document_id=2, ip='127.0.0.1', document_sha="e788144a95d952a46536b4731ae4624755aef9133a9e200e99fd2d8022a1795d").save()


def initial_vehicles(admin_user):
    from vehicles.models import Booking, Provider, VehicleType, Card, Location
    Provider(id=1, name="provider", description="---").save()
    Booking(id=1, unit_id=settings.ROOT_UNIT_PK, title="booking", responsible=admin_user, reason="why not?", provider_id=1,
            vehicletype=VehicleType.objects.create(provider_id=1, name="type", description="---"),
            card=Card.objects.create(provider_id=1, name="card", number="12345", description="---"),
            location=Location.objects.create(name="place", description="---"), start_date=datetime(2000, 01, 01), end_date=datetime(2099, 12, 31)).save()


def initial_logistics():
    from logistics.models import Room, RoomReservation, Supply, SupplyReservation, SupplyReservationLine 
    Room(id=1, title='room', description='description', unit_id=settings.ROOT_UNIT_PK).save()
    Supply(id=1, title='supply', description='description', unit_id=settings.ROOT_UNIT_PK).save()
    RoomReservation(id=1, room_id=1, title="needed", start_date=datetime(2000, 01, 01), end_date=datetime(2099, 12, 31), reason="because").save() 
    SupplyReservation(id=1, title="needed", start_date=datetime(2000, 01, 01), end_date=datetime(2099, 12, 31), contact_phone="0123456789", reason="because").save()
    SupplyReservationLine(id=1, supply_reservation_id=1, supply_id=1).save()


def initial_data():
    admin_user = initial_users_units()
    initial_main(admin_user)
    initial_vehicles(admin_user)
    initial_logistics()


class TruffeTestAbstract(TestCase, Client):

    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        Client.__init__(self)

    def setUp(self):
        TestCase.setUp(self)
        initial_data()

    def connect_admin(self):
        self.call('/users/login')
        csr_token_input = self.content.findAll('input', {'name': 'csrfmiddlewaretoken'})[0]           
        self.call('/users/login', {'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csr_token_input}, 'post', status_expected=302)
        
    def call(self, path, data={}, method='get', status_expected=200):
        self.response = getattr(self, method.lower(), self.get)(path, data, content_type=MULTIPART_CONTENT)
        try:
            self.content = BeautifulSoup(self.response.content, "html.parser")
        except Exception:
            self.content = self.response.content
        if status_expected != 0:
            self.assertEqual(self.response.status_code, status_expected, "HTTP error [%s]:%s" % (self.response.status_code, self.get_div('text-center error-box')))

    def call_check_redirect(self, path, data={}, method='get'):
        self.call(path, data, method, status_expected=302)
        self.assertRedirects(self.response, '/users/login?next=%s' % path)        

    def call_check_alert(self, path, data={}, method='get', alert_expected=None):
        self.call(path, data, method)
        alert_dom = self.get_div('alert alert-danger')
        self.assertEqual(alert_dom, alert_expected)

    def get_div(self, class_to_find):
        try:
            div_dom = self.content.findAll('div', {'class': class_to_find})
            return "\n".join([item.text.strip() for item in div_dom])
        except Exception:
            return None
