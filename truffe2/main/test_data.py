# -*- coding: utf-8 -*-
'''
Unit test tools for truffe

'''
from south.utils.datetime_utils import datetime

from django.conf import settings
from django.utils import timezone

from users.models import TruffeUser


def initial_users_units():
    from units.models import Unit, Role, Accreditation
    now = timezone.now()
    admin_user = TruffeUser.objects.create_superuser(username='admin', password='admin', first_name='admin', last_name='admin')
    admin_user.mobile = "0123456789"
    admin_user.adresse = "rue machin"
    admin_user.nom_banque = "Postfinance"
    admin_user.iban_ou_ccp = "0009876543210"
    admin_user.save()
    Unit(id=2, name='My unit', description='unit very nice', is_commission=True, is_equipe=True).save()
    user1 = TruffeUser.objects.create_user(username='user1', password='user1', first_name='user1', last_name='user1')
    user1.mobile = "0123456789"
    user1.adresse = "rue machin"
    user1.nom_banque = "Postfinance"
    user1.iban_ou_ccp = "0009876543210"
    user1.save()
    user2 = TruffeUser.objects.create_user(username='user2', password='user2', first_name='user2', last_name='user2')
    user2.mobile = "0123456789"
    user2.adresse = "rue machin"
    user2.nom_banque = "Postfinance"
    user2.iban_ou_ccp = "0009876543210"
    user2.save()
    user3 = TruffeUser.objects.create_user(username='user3', password='user3', first_name='user3', last_name='user3')
    user3.mobile = "0123456789"
    user3.adresse = "rue machin"
    user3.nom_banque = "Postfinance"
    user3.iban_ou_ccp = "0009876543210"
    user3.save()
    
    Role(id=1, name="role0", order=1, need_validation=False).save()
    Role(id=2, name="role1", order=2, need_validation=False, access='PRESIDENCE').save()
    Role(id=3, name="role2", order=3, need_validation=False, access='TRESORERIE').save()
    Role(id=4, name="role3", order=4, need_validation=False, access='SECRETARIAT').save()
    Accreditation(unit_id=settings.ROOT_UNIT_PK, user=admin_user, role_id=1, need_validation=True).save()
    Accreditation(unit_id=2, user=user1, role_id=2, need_validation=False).save()
    Accreditation(unit_id=2, user=user2, role_id=3, need_validation=False).save()
    Accreditation(unit_id=2, user=user3, role_id=4, need_validation=False).save()
    system_user = TruffeUser(pk=settings.SYSTEM_USER_PK, username='system', first_name='system', last_name='system',
                             is_active=True, is_superuser=True, last_login=now, date_joined=now)
    system_user.set_password('system')
    system_user.save()
    return admin_user


def initial_main(user):
    from main.models import File, SignableDocument, Signature
    File(id=1, title='title', description='descripption', file='sound/bigbox.mp3', access='all', group='misc').save()
    SignableDocument(id=1, title='unsigned', description='description', file='sound/messagebox.mp3', active=True).save()
    SignableDocument(id=2, title='signed', description='description', file='sound/smallbox.mp3', active=True).save()
    Signature(user=user, document_id=2, ip='127.0.0.1', document_sha="e788144a95d952a46536b4731ae4624755aef9133a9e200e99fd2d8022a1795d").save()


def initial_vehicles(user):
    from vehicles.models import Booking, Provider, VehicleType, Card, Location
    Provider(id=1, name="provider", description="---").save()
    Booking(id=1, unit_id=settings.ROOT_UNIT_PK, title="booking", responsible=user, reason="why not?", provider_id=1,
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


def initial_communication():
    from communication.models import AgepSlide, Display
    AgepSlide(title="slide", picture="img/logo_testing.png", unit_id=settings.ROOT_UNIT_PK, status='2_online').save()
    Display(id=1, title='display', description='display', unit_id=1).save()

    
def initial_notifications(user):    
    from notifications.models import Notification
    Notification(pk=1, key="mynotifkey", species="moderation", linked_object=user, user=user).save()


def initial_members(user):
    from members.models import MemberSet, Membership
    MemberSet(pk=1, name='default set', unit_id=settings.ROOT_UNIT_PK, api_secret_key='Secret123!').save()
    Membership(user=user, group_id=1, payed_fees=True).save()


def initial_accounting_core():
    from accounting_core.models import AccountingYear, Account, CostCenter, AccountCategory, TVA
    now = timezone.now()
    AccountingYear(id=1, name='current', start_date=datetime(now.year, 1, 1), end_date=datetime(now.year, 12, 31)).save()
    CostCenter(id=1, name='center', account_number='123', unit_id=settings.ROOT_UNIT_PK, accounting_year_id=1).save()
    AccountCategory(id=1, name="cat1", parent_hierarchique=None, order=1, accounting_year_id=1).save()
    AccountCategory(id=2, name="cat2", parent_hierarchique=None, order=2, accounting_year_id=1).save()
    AccountCategory(id=3, name="cat3", parent_hierarchique=None, order=3, accounting_year_id=1).save()
    Account(id=1, name='account1', account_number='1000', visibility='all', category_id=1, accounting_year_id=1).save()
    Account(id=2, name='account2', account_number='2000', visibility='cdd', category_id=1, accounting_year_id=1).save()
    Account(id=3, name='account3', account_number='3000', visibility='root', category_id=1, accounting_year_id=1).save()
    Account(id=4, name='account4', account_number='4000', visibility='all', category_id=2, accounting_year_id=1).save()
    Account(id=5, name='account5', account_number='5000', visibility='cdd', category_id=2, accounting_year_id=1).save()
    Account(id=6, name='account6', account_number='6000', visibility='root', category_id=2, accounting_year_id=1).save()
    Account(id=7, name='account7', account_number='7000', visibility='all', category_id=3, accounting_year_id=1).save()
    Account(id=8, name='account8', account_number='8000', visibility='cdd', category_id=3, accounting_year_id=1).save()
    Account(id=9, name='account9', account_number='9000', visibility='root', category_id=3, accounting_year_id=1).save()
    TVA(id=1, name='TVA1', value=10.0, agepoly_only=True, account_id=3, code='aaa').save()
    TVA(id=2, name='TVA2', value=15.0, agepoly_only=False, account_id=7, code='bbb').save()


def initial_accounting_main():    
    from accounting_main.models import Budget, BudgetLine, AccountingError, AccountingLine 
    Budget(id=1, name='my budget', unit_id=settings.ROOT_UNIT_PK, accounting_year_id=1, costcenter_id=1).save()
    BudgetLine(budget_id=1, account_id=1, amount=11.11, description="budget #1").save()
    BudgetLine(budget_id=1, account_id=2, amount=22.22, description="budget #2").save()
    BudgetLine(budget_id=1, account_id=3, amount=33.33, description="budget #3").save()
    BudgetLine(budget_id=1, account_id=4, amount=44.44, description="budget #4").save()
    BudgetLine(budget_id=1, account_id=5, amount=55.55, description="budget #5").save()
    BudgetLine(budget_id=1, account_id=6, amount=66.66, description="budget #6").save()
    BudgetLine(budget_id=1, account_id=7, amount=77.77, description="budget #7").save()
    BudgetLine(budget_id=1, account_id=8, amount=88.88, description="budget #8").save()
    BudgetLine(budget_id=1, account_id=9, amount=99.99, description="budget #9").save()
    AccountingError(id=1, accounting_year_id=1, costcenter_id=1).save()


def initial_accounting_tools(user):
    from accounting_tools.models import Withdrawal, InternalTransfer, FinancialProvider, Subvention
    from accounting_tools.models import ProviderInvoice, Invoice, CashBook, CashBookLine, ExpenseClaim, ExpenseClaimLine, ExpenseClaimLogging
    now = timezone.now()
    Withdrawal(id=1, name='reason', user=user, amount=12.34, desired_date=now, withdrawn_date=None, accounting_year_id=1, costcenter_id=1).save()
    InternalTransfer(id=1, name='reason', account_id=4, cost_center_from_id=1, cost_center_to_id=1, amount=98.76, transfert_date=now, accounting_year_id=1, status='3_archive').save()
    FinancialProvider(id=1, name='Financial name', tva_number='123456', iban_ou_ccp='ABCDEFG', bic='XYZ', address='Rue Des Arc en Ciel 25 - Case Postale 2, CH-1015 Lausanne').save()
    Subvention(id=1, name='Subvention', amount_asked=456, kind='subvention', linked_budget_id=1, accounting_year_id=1, unit_id=1).save()
    ProviderInvoice(id=1, name='Provider invoice', user=user, currency='EUR', provider_id=1, accounting_year_id=1, costcenter_id=1).save()
    Invoice(id=1, title='invoice', accounting_year_id=1, costcenter_id=1).save()
    CashBook(id=1, name='cash', user=user, nb_proofs=1, accounting_year_id=1, costcenter_id=1, status='6_archived').save()
    CashBookLine(cashbook_id=1, date=now, helper='2_sell', label='sell', account_id=2, value=123, tva=0, value_ttc=123).save()
    CashBookLine(cashbook_id=1, date=now, helper='1_deposit', label='deposit', account_id=7, value=123, tva=0, value_ttc=123).save()
    ExpenseClaim(id=1, name='expense', user=user, nb_proofs=1, accounting_year_id=1, costcenter_id=1, status='6_archived').save()
    ExpenseClaimLine(expense_claim_id=1, label='claim', account_id=5, value=54.65, tva=0, value_ttc=54.65).save()
    ExpenseClaimLogging(object_id=1, when=now, who=user, what='created').save()


def initial_data():
    admin_user = initial_users_units()
    initial_main(admin_user)
    initial_vehicles(admin_user)
    initial_logistics()
    initial_communication()
    initial_notifications(admin_user)
    initial_members(admin_user)
    initial_accounting_core()
    initial_accounting_main()
    initial_accounting_tools(admin_user)

