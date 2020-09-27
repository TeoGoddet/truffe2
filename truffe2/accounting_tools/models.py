# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.utils import translation
from django.utils.timezone import now
from raven.contrib.django.models import client
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat


import datetime
import string
from PIL import Image, ImageDraw, ImageFont
import os
from iso4217 import Currency
from accounting_tools.qrbill import QRBill  # Python 2
# from qrbill.bill import QRBill  # Python 3


from accounting_core.models import AccountingGroupModels
from accounting_core.utils import AccountingYearLinked, CostCenterLinked
from app.utils import get_current_year, get_current_unit
from generic.models import GenericModel, GenericStateModel, FalseFK, GenericContactableModel, GenericGroupsModel, GenericExternalUnitAllowed, GenericModelWithLines, ModelUsedAsLine, GenericModelWithFiles, GenericTaggableObject, GenericAccountingStateModel, LinkedInfoModel, SearchableModel
from notifications.utils import notify_people, unotify_people
from rights.utils import UnitExternalEditableModel, UnitEditableModel, AgepolyEditableModel


class _Subvention(GenericModel, GenericModelWithFiles, GenericModelWithLines, AccountingYearLinked, GenericStateModel, GenericGroupsModel, UnitExternalEditableModel, GenericExternalUnitAllowed, GenericContactableModel, SearchableModel):

    SUBVENTION_TYPE = (
        ('subvention', _(u'Subvention')),
        ('sponsorship', _(u'Sponsoring')),
    )

    class MetaRightsUnit(UnitExternalEditableModel.MetaRightsUnit):
        access = 'TRESORERIE'
        world_ro_access = False

    name = models.CharField(_(u'Nom du projet'), max_length=255)
    amount_asked = models.IntegerField(_(u'Montant demandé'))
    amount_given = models.IntegerField(_(u'Montant attribué'), blank=True, null=True)
    mobility_asked = models.IntegerField(_(u'Montant mobilité demandé'), blank=True, null=True)
    mobility_given = models.IntegerField(_(u'Montant mobilité attribué'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    comment_root = models.TextField(_('Commentaire AGEPoly'), blank=True, null=True)
    kind = models.CharField(_(u'Type de soutien'), max_length=15, choices=SUBVENTION_TYPE, blank=True, null=True)
    linked_budget = FalseFK('accounting_main.models.Budget', verbose_name=_(u'Budget annuel lié'), blank=True, null=True)

    class Meta:
        abstract = True
        # unique_together = (("unit", "unit_blank_name", "accounting_year"),)

    class MetaEdit:
        only_if = {
            'linked_budget': lambda (obj, user): obj.unit,
        }

        files_title = _(u'Fichiers')
        files_help = _(u"""Envoie les fichiers nécessaires pour ta demande de subvention, les demandes incomplètes ne seront pas considérées.<br />
En cas de question, merci de contacter <a href="mailto:administration@agepoly.ch">administration@agepoly.ch</a>.<br /><br />
Vous devez inclure dans votre demande au moins :
<ul>
                       <li>Budget du projet. Un document complémentaire détaillant et expliquant le budget est vivement recommandé.</li>
    <li>Bilans et comptes des d'activité des années précédentes</li>
    <li>Documents officiels (pour les Association hors AGEPoly) : statuts, liste des membres du comité, PV de la dernière AG</li>
</ul>
Ces différents documents sont demandés au format PDF dans la mesure du possible, afin d'éviter les problèmes d'ouvertures et de mise en page.""")

    class MetaData:
        list_display = [
            ('name', _(u'Projet')),
            ('get_unit_name', _(u'Association / Commission')),
            ('amount_asked', _(u'Montant demandé')),
            ('mobility_asked', _(u'Mobilité demandé')),
            ('status', _(u'Statut')),
        ]

        default_sort = "[2, 'asc']"  # unit
        filter_fields = ('name', 'unit__name', 'unit_blank_name')

        details_display = list_display + [('description', _(u'Description')), ('accounting_year', _(u'Année comptable'))]
        details_display.insert(3, ('amount_given', _(u'Montant attribué')))
        details_display.insert(5, ('mobility_given', _(u'Montant mobilité attribué')))
        extra_right_display = {'comment_root': lambda (obj, user): obj.rights_can('LIST', user)}

        files_title = _(u'Fichiers')
        base_title = _(u'Subvention')
        list_title = _(u'Liste des demandes de subvention')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-gift'

        menu_id = 'menu-compta-subventions'
        not_sortable_columns = ['get_unit_name']
        safe_fields = ['get_unit_name']

        has_unit = True

        forced_widths = {
            '3': '150px',
            '4': '150px',
        }

        help_list = _(u"""Les demandes de subvention peuvent être faites par toutes les commissions ou associations auprès de l'AGEPoly.""")

    class MetaAccounting:
        copiable = False

    class MetaLines:
        lines_objects = [
            {
                'title': _(u'Evènements'),
                'class': 'accounting_tools.models.SubventionLine',
                'form': 'accounting_tools.forms.SubventionLineForm',
                'related_name': 'events',
                'field': 'subvention',
                'sortable': True,
                'date_fields': ['start_date', 'end_date'],
                'show_list': [
                    ('name', _(u'Titre')),
                    ('start_date', _(u'Du')),
                    ('end_date', _(u'Au')),
                    ('place', _(u'Lieu')),
                    ('nb_spec', _(u'Nb personnes attendues')),
                ]
            },
        ]

    class MetaState:

        states = {
            '0_draft': _(u'Brouillon'),
            '0_correct': _(u'A corriger'),
            '1_submited': _(u'Demande soumise'),
            '2_treated': _(u'Demande traitée'),
        }

        default = '0_draft'

        states_texts = {
            '0_draft': _(u'La demande est en cours de création et n\'est pas publique.'),
            '1_submited': _(u'La demande a été soumise.'),
            '0_correct': _(u'La demande doit être corrigée.'),
            '2_treated': _(u'La demande a été traitée.'),
        }

        states_links = {
            '0_draft': ['1_submited'],
            '0_correct': ['1_submited'],
            '1_submited': ['2_treated', '0_correct'],
            '2_treated': [],
        }

        states_colors = {
            '0_draft': 'primary',
            '1_submited': 'default',
            '0_correct': 'warning',
            '2_treated': 'success',
        }

        states_icons = {
            '0_draft': '',
            '1_submited': '',
            '0_correct': '',
            '2_treated': '',
        }

        list_quick_switch = {
            '0_draft': [('1_submited', 'fa fa-check', _(u'Soumettre la demande'))],
            '0_correct': [('1_submited', 'fa fa-check', _(u'Soumettre la demande'))],
            '1_submited': [('2_treated', 'fa fa-check', _(u'Marquer la demande comme traitée')), ('0_correct', 'fa fa-exclamation', _(u'Demander des corrections'))],
            '2_treated': [],
        }

        forced_pos = {
            '0_draft': (0.2, 0.15),
            '0_correct': (0.5, 0.85),
            '1_submited': (0.5, 0.15),
            '2_treated': (0.8, 0.15),
        }

        states_default_filter = '0_draft,0_correct'
        status_col_id = 5

        class SubventionValidationForm(forms.Form):
            amount_given = forms.IntegerField(label=_(u'Montant accordé'))
            mobility_given = forms.IntegerField(label=_(u'Montant mobilité accordé'))

        states_bonus_form = {
            '2_treated': SubventionValidationForm
        }

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u""

        index_files = True

        fields = [
            'name',
            'description',
            'comment_root',
            'amount_asked',
            'amount_given',
            'mobility_asked',
            'mobility_given',
        ]

        linked_lines = {
            'events': ['name', 'place']
        }

    def __init__(self, *args, **kwargs):
        super(_Subvention, self).__init__(*args, **kwargs)

        self.MetaRights = type("MetaRights", (self.MetaRights,), {})
        self.MetaRights.rights_update({
            'EXPORT': _(u'Peut exporter les éléments'),
        })

    def switch_status_signal(self, request, old_status, dest_status):

        s = super(_Subvention, self)

        if hasattr(s, 'switch_status_signal'):
            s.switch_status_signal(request, old_status, dest_status)

        if dest_status == '2_treated':
            self.amount_given = request.POST.get('amount_given', self.amount_given)
            self.mobility_given = request.POST.get('mobility_given', self.mobility_given)
            self.save()

    def may_switch_to(self, user, dest_state):
        return self.rights_can('EDIT', user) and super(_Subvention, self).may_switch_to(user, dest_state)

    def can_switch_to(self, user, dest_state):

        if self.status == '0_draft' and self.accounting_year.subvention_deadline and self.accounting_year.subvention_deadline < now() and not self.rights_in_root_unit(user, self.MetaRightsUnit.access):
            return (False, _(u'Le délait est dépassé pour les subventions !'))

        if self.status == '2_treated' and not user.is_superuser:
            return (False, _(u'Seul un super utilisateur peut sortir cet élément de l\'état traité'))

        if int(dest_state[0]) - int(self.status[0]) != 1 and not user.is_superuser:
            if not (self.status == '1_submited' and dest_state == '0_correct'):  # Exception faite de la correction
                return (False, _(u'Seul un super utilisateur peut sauter des étapes ou revenir en arrière.'))

        if self.status == '1_submited' and not self.rights_in_root_unit(user, self.MetaRightsUnit.access):
            return (False, _(u'Seul un membre du Comité de Direction peut marquer la demande comme traitée ou à corriger.'))

        if not self.rights_can('EDIT', user):
            return (False, _('Pas les droits.'))

        return super(_Subvention, self).can_switch_to(user, dest_state)

    def __unicode__(self):
        return u"{} {}".format(self.get_real_unit_name(), self.accounting_year)

    def genericFormExtraClean(self, data, form):
        """Check that unique_together is fulfiled"""
        from accounting_tools.models import Subvention

        if Subvention.objects.exclude(pk=self.pk).filter(accounting_year=get_current_year(form.truffe_request), unit=get_current_unit(form.truffe_request), unit_blank_name=data['unit_blank_name'], deleted=False).count():
            raise forms.ValidationError(_(u'Une demande de subvention pour cette unité existe déjà pour cette année comptable.'))  # Potentiellement parmi les supprimées

    def genericFormExtraInit(self, form, current_user, *args, **kwargs):
        """Remove fields that should be edited by CDD only."""

        if not self.rights_in_root_unit(current_user, self.MetaRightsUnit.access):
            for key in ['amount_given', 'mobility_given', 'comment_root']:
                del form.fields[key]
            form.fields['kind'].widget = forms.HiddenInput()

    def rights_can_EXPORT(self, user):
        return self.rights_in_root_unit(user)

    def rights_can_EDIT(self, user):

        if self.status[0] != '0' and not self.rights_in_root_unit(user):
            return False

        return super(_Subvention, self).rights_can_EDIT(user)

    def get_real_unit_name(self):
        return self.unit_blank_name or self.unit.name

    def total_people(self):
        """Return the total number of expected people among all events"""
        total = 0
        for line in self.events.all():
            total += line.nb_spec
        return total


class SubventionLine(ModelUsedAsLine):
    name = models.CharField(_(u'Nom de l\'évènement'), max_length=255)
    start_date = models.DateField(_(u'Début de l\'évènement'))
    end_date = models.DateField(_(u'Fin de l\'évènement'))
    place = models.CharField(_(u'Lieu de l\'évènement'), max_length=100)
    nb_spec = models.PositiveIntegerField(_(u'Nombre de personnes attendues'))

    subvention = models.ForeignKey('Subvention', related_name="events", verbose_name=_(u'Subvention/sponsoring'))

    def __unicode__(self):
        return u"{}:{}".format(self.subvention.name, self.name)


class _Invoice(GenericModel, GenericStateModel, GenericTaggableObject, CostCenterLinked, GenericModelWithLines, GenericGroupsModel, GenericContactableModel, AccountingYearLinked, UnitEditableModel, SearchableModel):
    """Modèle pour les factures"""

    class MetaRightsUnit(UnitEditableModel.MetaRightsUnit):
        access = ['TRESORERIE', 'SECRETARIAT']

    class MetaRights(UnitEditableModel.MetaRights):
        linked_unit_property = 'costcenter.unit'

    def __init__(self, *args, **kwargs):
        super(_Invoice, self).__init__(*args, **kwargs)

        self.MetaRights.rights_update({
            'DOWNLOAD_PDF': _(u'Peut exporter la facture en PDF'),
        })

    title = models.CharField(max_length=140)

    client_name = models.CharField(_('Nom du client'), help_text=_(u'Exemple: \'Licorne SA - Monsieur Poney\''), max_length=70)
    address = models.CharField(_('Adresse'), help_text=_(u'Format: \'Rue Des Arc en Ciel 25 - Case Postale 2, CH-1015 Lausanne\''), max_length=140, blank=True, null=True)

    date_and_place = models.CharField(_(u'Lieu et date'), max_length=512, blank=True, null=True)
    preface = models.TextField(_(u'Introduction'), help_text=_(u'Texte affiché avant la liste. Exemple: \'Pour l\'achat du Yearbook 2014\' ou \'Chère Madame, - Par la présente, je me permets de vous remettre notre facture pour le financement de nos activités associatives pour l\'année académique 2014-2015.\''), blank=True, null=True)
    ending = models.TextField(_(u'Conclusion'), help_text=_(u'Affiché après la liste, avant les moyens de paiements'), max_length=1024, blank=True, null=True)
    display_qr = models.BooleanField(_(u'Afficher la QR Facture'), help_text=_(u'Affiche la QR Facture dans le PDF.'), default=True)
    greetings = models.CharField(_(u'Salutations'), default='', max_length=1024, blank=True, null=True)
    sign = models.TextField(_(u'Signature'), help_text=_(u'Titre de la zone de signature'), blank=True, null=True)
    annex = models.BooleanField(_(u'Annexes'), help_text=_(u'Affiche \'Annexe(s): ment.\' en bas de la facture'), default=False)
    delay = models.SmallIntegerField(_(u'Délai de paiement en jours'), default=30, help_text=_(u'Mettre zéro pour cacher le texte. Il s\'agit du nombre de jours de délai pour le paiement.'))
    english = models.BooleanField(_(u'Anglais'), help_text=_(u'Génére la facture en anglais'), default=False)
    reception_date = models.DateField(_(u'Date valeur banque'), help_text=_(u'Date de la réception du paiement au niveau de la banque'), blank=True, null=True)
    add_to = models.BooleanField(_(u'Rajouter "À l\'attention de"'), default=False)

    class MetaData:
        list_display = [
            ('title', _('Titre')),
            ('get_creation_date', _(u'Date de création')),
            ('reception_date', _(u'Date valeur banque')),
            ('status', _('Statut')),
            ('costcenter', _(u'Centre de coût')),
            ('get_qr_ref', _(u'Référence')),
            ('get_total_display', _(u'Total')),
        ]
        details_display = list_display + [
            ('client_name', _('Nom Client')),
            ('address', _('Adresse')),
            ('date_and_place', _(u'Lieu et date')),
            ('preface', _(u'Introduction')),
            ('ending', _(u'Conclusion')),
            ('display_qr', _(u'Afficher la QR Facture')),
            ('delay', _(u'Délai de paiement en jours')),
            ('greetings', _(u'Salutations')),
            ('sign', _(u'Signature')),
            ('annex', _(u'Annexes')),
            ('english', _(u'Facture en anglais')),
            ('add_to', _(u'Rajouter "À l\'attention de"')),

        ]
        filter_fields = ('title', 'client_name')

        base_title = _(u'Facture')
        list_title = _(u'Liste de toutes les factures')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-pencil-square-o'

        default_sort = "[2, 'desc']"  # creation_date (pk)

        menu_id = 'menu-compta-invoice'

        has_unit = True

        help_list = _(u"""Les factures te permettent de demander de l'argent à, par exemple, une entreprise. Tu DOIS déclarer toutes les factures que tu envoies via cet outil (tu n'es pas obligé d'utiliser le PDF généré, à condition qu'il contienne TOUTES LES INFORMATIONS NÉCESSAIRES).""")

        trans_sort = {'get_creation_date': 'pk'}

        not_sortable_columns = ['get_reference', 'get_total_display']
        yes_or_no_fields = ['display_qr', 'annex', 'english', 'add_to']
        datetime_fields = ['get_creation_date', 'reception_date']

    class MetaEdit:

        date_fields = ['reception_date']

        @staticmethod
        def set_extra_defaults(obj, request):
            obj.sign = u'{} {}'.format(request.user.first_name, request.user.last_name)

            with translation.override('fr'):
                obj.date_and_place = u'Lausanne, le {}'.format(_date(datetime.datetime.now(), u'd F Y'))

        only_if = {
            'reception_date': lambda (obj, user): user.is_superuser or obj.rights_in_root_unit(user, access='TRESORERIE'),
        }

    class MetaLines:
        lines_objects = [
            {
                'title': _(u'Lignes'),
                'class': 'accounting_tools.models.InvoiceLine',
                'form': 'accounting_tools.forms.InvoiceLineForm',
                'related_name': 'lines',
                'field': 'invoice',
                'sortable': True,
                'tva_fields': ['tva'],
                'show_list': [
                    ('label', _(u'Titre')),
                    ('quantity', _(u'Quantité')),
                    ('value', _(u'Montant unitaire (HT)')),
                    ('get_tva', _(u'TVA')),
                    ('total', _(u'Montant (TTC)')),
                ]},
        ]

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u""

        fields = [
            'address',
            'date_and_place',
            'ending',
            'greetings',
            'preface',
            'sign',
            'title',
            'get_reference',
            'get_qr_ref',
            'reception_date',
        ]

        linked_lines = {
            'lines': ['label', 'value_ttc', 'total']
        }

    class MetaState:

        states = {
            '0_preparing': _(u'En préparation'),
            '0_correct': _(u'Corrections nécessaires'),
            '2_ask_accord': _(u'Attente Accord AGEPoly'),
            '2_accord': _(u'Attente Envoi'),
            '3_sent': _(u'Envoyée / paiement en attente'),
            '4_archived': _(u'Archivée / Paiement reçu'),
            '5_canceled': _(u'Annulée'),
        }

        default = '0_preparing'

        states_texts = {
            '0_preparing': _(u'La facture est en cours de rédaction'),
            '0_correct': _(u'La facture doit être corrigée'),
            '2_ask_accord': _(u'Il faut attendre l\'accord de l\'AGEPoly'),
            '2_accord': _(u'Il faut envoyer la facture'),
            '3_sent': _(u'La facture a été envoyée, le paiement est en attente. La facture n\'est plus éditable !'),
            '4_archived': _(u'Le paiement de la facture a été reçu, le processus de facturation est terminé.'),
            '5_canceled': _(u'La facture a été annulée'),
        }

        states_links = {
            '0_preparing': ['2_ask_accord', '5_canceled'],
            '0_correct': ['2_ask_accord', '5_canceled'],
            '2_ask_accord': ['0_correct', '2_accord', '5_canceled'],
            '2_accord': ['0_correct', '3_sent', '4_archived', '5_canceled'],
            '3_sent': ['0_correct', '4_archived', '5_canceled'],
            '4_archived': [],
            '5_canceled': [],
        }

        states_colors = {
            '0_preparing': 'primary',
            '0_correct': 'danger',
            '2_ask_accord': 'primary',
            '2_accord': 'info',
            '3_sent': 'warning',
            '4_archived': 'success',
            '5_canceled': 'default',
        }

        states_icons = {
        }

        list_quick_switch = {
            '0_preparing': [('2_ask_accord', 'fa fa-question', _(u'Demande accord AGEPoly'))],
            '0_correct': [('2_ask_accord', 'fa fa-question', _(u'Demande accord AGEPoly'))],
            '2_ask_accord': [('2_accord', 'fa fa-check', _(u'Donner l\'accord')),],
            '2_accord': [('3_sent', 'fa fa-check', _(u'Marquer comme envoyée')),],
            '3_sent': [('4_archived', 'fa fa-check', _(u'Marquer comme terminée')),],
            '4_archived': [],
            '5_canceled': [],
        }

        states_quick_switch = {
            '0_preparing': [('2_ask_accord', _(u'Demande accord AGEPoly'))],
            '0_correct': [('2_ask_accord', _(u'Demande accord AGEPoly'))],
            '2_ask_accord': [('2_accord', _(u'Donner l\'accord'))],
            '2_accord': [('3_sent', _(u'Marquer comme envoyée'))],
            '3_sent': [('4_archived', _(u'Marquer comme terminée')), ],
            '4_archived': [],
            '5_canceled': [],
        }
        states_default_filter = '0_preparing,2_ask_accord,2_accord,3_sent'
        states_default_filter_related = '0_preparing,2_ask_accord,2_accord,3_sent'
        status_col_id = 1

        forced_pos = {
            '0_preparing': (0.1, 0.15),
            '0_correct': (0.5, 0.85),
            '2_ask_accord': (0.26, 0.15),
            '2_accord': (0.5, 0.15),
            '3_sent': (0.7, 0.35),
            '4_archived': (0.9, 0.15),
            '5_canceled': (0.9, 0.85),
        }

        def build_form_date(request, obj):
            class FormDate(forms.Form):
                date = forms.DateField(label=_('Date valeur banque'), required=False, initial=now())

                def __init__(self, *args, **kwargs):

                    super(FormDate, self).__init__(*args, **kwargs)

                    self.fields['date'].widget.attrs = {'is_date': 'true'}

            return FormDate

        states_bonus_form = {
            '4_archived': build_form_date
        }

    def switch_status_signal(self, request, old_status, dest_status):

        s = super(_Invoice, self)

        if hasattr(s, 'switch_status_signal'):
            s.switch_status_signal(request, old_status, dest_status)

        if dest_status == '0_correct':
            notify_people(request, '%s.to_correct' % (self.__class__.__name__,), 'invoices_to_correct', self, self.build_group_members_for_editors())

        if dest_status == '2_ask_accord':
            notify_people(request, '%s.validable' % (self.__class__.__name__,), 'accounting_validable', self, self.people_in_root_unit(['TRESORERIE', 'SECRETARIAT']))

        if dest_status == '2_accord':
            notify_people(request, '%s.accepted' % (self.__class__.__name__,), 'invoices_accepted', self, self.build_group_members_for_editors())

        if dest_status == '3_sent':
            notify_people(request, '%s.sent' % (self.__class__.__name__,), 'invoices_sent', self, self.build_group_members_for_editors())

        if dest_status == '4_archived':
            unotify_people('%s.sent' % (self.__class__.__name__,), self)
            notify_people(request, '%s.done' % (self.__class__.__name__,), 'invoices_done', self, self.build_group_members_for_editors())

            if request.POST.get('date'):
                self.reception_date = request.POST['date']
                self.save()

    def may_switch_to(self, user, dest_state):

        if dest_state == '0_preparing' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return False

        if dest_state == '2_accord' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return False

        if dest_state == '4_archived' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return False

        return super(_Invoice, self).rights_can_EDIT(user) and super(_Invoice, self).may_switch_to(user, dest_state)

    def can_switch_to(self, user, dest_state):

        if not super(_Invoice, self).rights_can_EDIT(user):
            return (False, _('Pas les droits.'))

        if self.status == '3_sent' and dest_state[0] == '0' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return (False, _('Seul l\'AGEPoly peut modifier une facture une fois qu\'elle a été envoyée.'))

        if dest_state == '2_accord' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return (False, _('Seul l\'AGEPoly peut valider une facture.'))

        if dest_state == '4_archived' and not user.is_superuser and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return (False, _('Seul l\'AGEPoly peut archiver une facture.'))

        return super(_Invoice, self).can_switch_to(user, dest_state)

    def rights_can_EDIT(self, user):
        # On ne peut pas éditer les factures envoyés/reçues

        if self.status == '2_accord' and (user.is_superuser or self.rights_in_root_unit(user, 'SECRETARIAT')):
            return True

        if self.status in ['0_preparing', '0_correct']:
            return super(_Invoice, self).rights_can_EDIT(user)

        return False

    def rights_can_DISPLAY_LOG(self, user):
        """Always display log, even if current state dosen't allow edit"""
        return super(_Invoice, self).rights_can_EDIT(user)

    def rights_can_DOWNLOAD_PDF(self, user):
        if user.is_superuser:
            return True

        if self.rights_in_root_unit(user, 'TRESORERIE') or self.rights_in_root_unit(user, 'SECRETARIAT'):
            return True

        if self.rights_can_SHOW(user) and self.status in ['2_accord', '3_sent', '4_archived']:
            return True

        return False


    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.get_reference())

    @property
    def multiline_address(self):
        return self.address.replace(u',', u'\n')

    def get_reference(self):
        return 'TR2-{}-{}'.format(self.costcenter.account_number, self.pk)

    def get_qr_ref(self):
        ref = '{0:06d}{1:06d}{2:06d}'.format(int(self.costcenter.account_number.replace('.', '')) % 100000, int(self.pk / 100000), self.pk % 100000)

        # modulo 97-10 (same as iban)
        checkdigits = 98 - int('29272{0}271500'.format(ref)) % 97  # TR2 -> 29272 et RF00 -> 271500
        if (checkdigits < 10):
            checkdigits = '0{}'.format(checkdigits)
        else:
            checkdigits = unicode(checkdigits)

        return 'RF{0} TR2{1} {2} {3} {4} {5} {6}'.format(checkdigits, ref[0], ref[1:5], ref[5:9], ref[9:13], ref[13:17], ref[17])

    def get_lines(self):
        return self.lines.order_by('order').all()

    def get_total(self):
        return sum([line.total() for line in self.get_lines()])

    def get_total_ht(self):
        return sum([line.get_total_ht() for line in self.get_lines()])

    def get_total_display(self):
        return '{} CHF'.format(intcomma(floatformat(self.get_total(), 2)))

    def generate_QR(self):
        address = self.multiline_address.splitlines()
        bill = QRBill(
            account='CH1904835028789771000',
            amount=unicode(self.get_total()),
            currency='CHF',
            debtor={
                'name': self.client_name,
                'line1': address[0][0:70],
                'line2': address[1][0:70] if len(address) > 1 else '',
                'country': 'CH', #otherwise not accepted by some banks 
            },
            creditor={
                'name': u'Ass. Genérale Des Etudiants de l\'EPFL', 'street': u'Case Postale', 'house_num': u'16', 'pcode': u'1015', 'city': u'Lausanne', u'country': u'CH',
            },
            ref_number=self.get_qr_ref(),
            extra_infos=self.title,
            language='en' if self.english else 'fr',
            top_line=True,
            extra_auto_infos='//S1/10/{ref}/11/{date}/30/{tvauid}/40/0:{delay}/'.format(ref=self.get_reference(), date=now().strftime('%y%m%d'), tvauid='113397612', delay=self.delay)
        )
        return bill

    def get_language(self):

        return 'en-us' if self.english else 'fr-ch'


class InvoiceLine(ModelUsedAsLine):

    invoice = models.ForeignKey('Invoice', related_name="lines")

    label = models.CharField(_(u'Titre'), max_length=255)
    quantity = models.DecimalField(_(u'Quantité'), max_digits=20, decimal_places=0, default=1)
    value = models.DecimalField(_('Montant unitaire (HT)'), max_digits=20, decimal_places=2)
    tva = models.DecimalField(_('TVA'), max_digits=20, decimal_places=2)
    value_ttc = models.DecimalField(_('Montant (TTC)'), max_digits=20, decimal_places=2)

    def __unicode__(self):
        return u'{}: {} * ({} + {}% == {})'.format(self.label, self.quantity, self.value, self.tva, self.value_ttc)

    def total(self):
        return float(self.quantity) * float(self.value_ttc)

    def get_total_ht(self):
        return float(self.quantity) * float(self.value)

    def get_tva(self):
        from accounting_core.models import TVA
        return TVA.tva_format(self.tva)

    def get_tva_value(self):
        return float(self.quantity) * float(self.value) * float(self.tva) / 100.0


class _InternalTransfer(GenericModel, GenericStateModel, GenericTaggableObject, AccountingYearLinked, AgepolyEditableModel, GenericGroupsModel, GenericContactableModel, SearchableModel):
    """Modèle pour les transferts internes"""

    class MetaRightsAgepoly(AgepolyEditableModel.MetaRightsAgepoly):
        access = 'TRESORERIE'

    name = models.CharField(_('Raison du transfert'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    account = FalseFK('accounting_core.models.Account', verbose_name=_(u'Compte concerné'))
    cost_center_from = FalseFK('accounting_core.models.CostCenter', related_name='internal_transfer_from', verbose_name=_(u'Centre de coûts prélevé'))
    cost_center_to = FalseFK('accounting_core.models.CostCenter', related_name='internal_transfer_to', verbose_name=_(u'Centre de coûts versé'))
    amount = models.DecimalField(_('Montant'), max_digits=20, decimal_places=2)
    transfert_date = models.DateField(_('Date effective'), blank=True, null=True)

    class MetaData:
        list_display = [
            ('name', _('Raison')),
            ('account', _('Compte')),
            ('amount', _('Montant')),
            ('cost_center_from', _(u'De')),
            ('cost_center_to', _(u'Vers')),
            ('status', _('Statut')),
        ]

        details_display = list_display + [('transfert_date', _('Date effective')), ('description', _(u'Description')), ('accounting_year', _(u'Année comptable')), ]
        filter_fields = ('name', 'status', 'account__name', 'account__account_number', 'amount', 'cost_center_from__name', 'cost_center_from__account_number', 'cost_center_to__name', 'cost_center_to__account_number')

        base_title = _(u'Transferts internes')
        list_title = _(u'Liste des transferts internes')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-exchange'

        menu_id = 'menu-compta-transfert'

        help_list = _(u"""Les transferts internes permettent de déplacer de l'argent entre les entitées de l'AGEPoly sur un même compte.

Ils peuvent être utilisés dans le cadre d'une commande groupée ou d'un remboursement d'une unité vers l'autre.""")

        datetime_fields = ['transfert_date']

    class Meta:
        abstract = True

    class MetaGroups(GenericGroupsModel.MetaGroups):
        pass

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u""

        fields = [
            'account',
            'cost_center_to',
            'cost_center_from',
            'description',
            'name',
            'transfert_date',
        ]

    class MetaState:
        states = {
            '0_draft': _('Brouillon'),
            '1_agep_validable': _(u'Attente accord AGEPoly'),
            '2_accountable': _(u'A comptabiliser'),
            '3_archived': _(u'Archivé'),
            '3_canceled': _(u'Annulé'),
        }
        default = '0_draft'

        states_texts = {
            '0_draft': _(u'L\'objet est en cours de création.'),
            '1_agep_validable': _(u'L\'objet doit être accepté par l\'AGEPoly.'),
            '2_accountable': _(u'L\'objet est en attente d\'être comptabilisé.'),
            '3_archived': _(u'L\'objet est archivé. Il n\'est plus modifiable.'),
            '3_canceled': _(u'L\'objet a été annulé.'),
        }

        states_links = {
            '0_draft': ['1_agep_validable', '3_canceled'],
            '1_agep_validable': ['0_draft', '2_accountable', '3_canceled'],
            '2_accountable': ['0_draft', '3_archived', '3_canceled'],
            '3_archived': [],
            '3_canceled': [],
        }

        list_quick_switch = {
            '0_draft': [('1_agep_validable', 'fa fa-question', _(u'Demander accord AGEPoly')), ('3_canceled', 'fa fa-ban', _(u'Annuler')), ],
            '1_agep_validable': [('2_accountable', 'fa fa-check', _(u'Demander à comptabiliser')), ('3_canceled', 'fa fa-ban', _(u'Annuler'))],
            '2_accountable': [('3_archived', 'glyphicon glyphicon-remove-circle', _(u'Archiver')), ('3_canceled', 'fa fa-ban', _(u'Annuler'))],
        }

        states_colors = {
            '0_draft': 'primary',
            '1_agep_validable': 'default',
            '2_accountable': 'info',
            '3_archived': 'success',
            '3_canceled': 'danger',
        }

        states_icons = {
            '0_draft': '',
            '1_agep_validable': '',
            '2_accountable': '',
            '3_archived': '',
            '3_canceled': '',
        }

        states_default_filter = '0_draft,1_agep_validable'
        status_col_id = 6

        forced_pos = {
            '0_draft': (0.1, 0.15),
            '1_agep_validable': (0.36, 0.15),
            '2_accountable': (0.62, 0.15),
            '3_archived': (0.9, 0.15),
            '3_canceled': (0.9, 0.85),
        }

        def build_form_done(request, obj):
            class FormDone(forms.Form):
                transfert_date = forms.DateField(label=_('Date effective'), required=True, initial=now().date())

                def __init__(self, *args, **kwargs):

                    super(FormDone, self).__init__(*args, **kwargs)
                    self.fields['transfert_date'].widget.attrs = {'is_date': 'true'}

            return FormDone

        states_bonus_form = {
            '3_archived': build_form_done
        }

    class MetaEdit:
        date_fields = ['transfert_date']

    def may_switch_to(self, user, dest_state):

        if user.is_superuser:
            return (True, None)

        if self.status[0] == '3' and not user.is_superuser:
            return False

        if dest_state == '3_canceled' and super(_InternalTransfer, self).rights_can_EDIT(user):
            return True

        return super(_InternalTransfer, self).may_switch_to(user, dest_state) and super(_InternalTransfer, self).rights_can_EDIT(user)

    def can_switch_to(self, user, dest_state):

        if user.is_superuser:
            return (True, None)

        if self.status[0] == '3' and not user.is_superuser:
            return (False, _(u'Seul un super utilisateur peut sortir cet élément de l\'état archivé/annulé'))

        if dest_state == '3_canceled' and super(_InternalTransfer, self).rights_can_EDIT(user):
            return (True, None)

        if not super(_InternalTransfer, self).rights_can_EDIT(user):
            return (False, _('Pas les droits.'))

        return super(_InternalTransfer, self).can_switch_to(user, dest_state)

    def rights_can_SHOW(self, user):
        if self.rights_in_unit(user, self.cost_center_from.unit, access='TRESORERIE') or self.rights_in_unit(user, self.cost_center_to.unit, access='TRESORERIE'):
            return True

        return super(_InternalTransfer, self).rights_can_SHOW(user)

    def rights_can_LIST(self, user):
        return super(_InternalTransfer, self).rights_can_SHOW(user)

    def rights_can_DISPLAY_LOG(self, user):
        return self.rights_can_SHOW(user)

    def rights_can_EDIT(self, user):
        if int(self.status[0]) >= 2:
            return False

        return super(_InternalTransfer, self).rights_can_EDIT(user)

    def switch_status_signal(self, request, old_status, dest_status):

        s = super(_InternalTransfer, self)

        if hasattr(s, 'switch_status_signal'):
            s.switch_status_signal(request, old_status, dest_status)

        if dest_status == '1_agep_validable':
            notify_people(request, '%s.validable' % (self.__class__.__name__,), 'accounting_validable', self, self.people_in_root_unit('TRESORERIE'))
        elif dest_status == '2_accountable':
            unotify_people('%s.validable' % (self.__class__.__name__,), self)
            notify_people(request, '%s.accountable' % (self.__class__.__name__,), 'accounting_accountable', self, self.people_in_root_unit('SECRETARIAT'))
        elif dest_status[0] == '3':
            unotify_people('%s.accountable' % (self.__class__.__name__,), self)
            tresoriers = self.people_in_unit(self.cost_center_from.unit, 'TRESORERIE', no_parent=True) + self.people_in_unit(self.cost_center_to.unit, 'TRESORERIE', no_parent=True)
            notify_people(request, '%s.accepted' % (self.__class__.__name__,), 'accounting_accepted', self, list(set(tresoriers + self.build_group_members_for_editors())))

            if dest_status == '3_archived' and request.POST.get('transfert_date'):
                self.transfert_date = request.POST.get('transfert_date')
                self.save()

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.accounting_year)

    def genericFormExtraInit(self, form, current_user, *args, **kwargs):
        """Set querysets according to the selected accounting_year"""
        from accounting_core.models import Account, CostCenter

        form.fields['account'].queryset = Account.objects.filter(accounting_year=self.accounting_year).order_by('category__order')
        form.fields['cost_center_from'].queryset = CostCenter.objects.filter(accounting_year=self.accounting_year).order_by('account_number')
        form.fields['cost_center_to'].queryset = CostCenter.objects.filter(accounting_year=self.accounting_year).order_by('account_number')

    def genericFormExtraClean(self, data, form):
        if 'cost_center_from' in data and 'cost_center_to' in data and data['cost_center_from'] == data['cost_center_to']:
            raise forms.ValidationError(_(u'Les deux centres de coûts doivent être différents.'))


class _Withdrawal(GenericModel, GenericStateModel, GenericTaggableObject, GenericModelWithFiles, AccountingYearLinked, CostCenterLinked, UnitEditableModel, GenericGroupsModel, GenericContactableModel, LinkedInfoModel, SearchableModel):
    """Modèle pour les retraits cash"""

    class MetaRightsUnit(UnitEditableModel.MetaRightsUnit):
        access = ['TRESORERIE', 'SECRETARIAT']

    class MetaRights(UnitEditableModel.MetaRights):
        linked_unit_property = 'costcenter.unit'

    name = models.CharField(_('Raison du retrait'), max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'Responsable'))
    description = models.TextField(_('Description'), blank=True, null=True)
    amount = models.DecimalField(_('Montant'), max_digits=20, decimal_places=2)
    desired_date = models.DateField(_(u'Date souhaitée'))
    withdrawn_date = models.DateField(_(u'Date réelle de retrait'), blank=True, null=True)

    class MetaData:
        list_display = [
            ('name', _('Raison')),
            ('amount', _('Montant')),
            ('costcenter', _(u'Centre de coûts')),
            ('status', _('Statut')),
        ]

        details_display = list_display + [('user', _(u'Responsable')), ('description', _(u'Description')), ('desired_date', _(u'Date souhaitée')), ('withdrawn_date', _(u'Date retrait')), ('accounting_year', _(u'Année comptable')), ]
        filter_fields = ('name', 'status', 'amount', 'costcenter__name', 'costcenter__account_number', 'user__username', 'user__first_name', 'user__last_name')
        datetime_fields = ['desired_date', 'withdrawn_date']

        default_sort = "[0, 'desc']"  # Creation date (pk) descending

        base_title = _(u'Retraits cash')
        list_title = _(u'Liste des retraits cash')
        files_title = _(u'Pièces comptables')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-share-square-o'

        has_unit = True

        menu_id = 'menu-compta-rcash'

        help_list = _(u"""Les demandes de retrait cash doivent impérativement être remplies pour pouvoir retirer de l'argent depuis le compte d'une unité.

L'argent doit ensuite être justifié au moyen d'un journal de caisse.""")

    class Meta:
        abstract = True

    class MetaEdit:
        files_title = _(u'Pièces comptables')
        files_help = _(u'Pièces comptables liées au retrait cash.')
        date_fields = ['desired_date', 'withdrawn_date']

    class MetaGroups(GenericGroupsModel.MetaGroups):
        pass

    class MetaState:
        states = {
            '0_draft': _('Brouillon'),
            '1_agep_validable': _(u'Attente accord AGEPoly'),
            '2_withdrawn': _(u'Prêt à être récupéré'),
            '3_used': _(u'Récupéré / A justifier'),
            '4_archived': _(u'Archivé'),
            '4_canceled': _(u'Annulé'),
        }
        default = '0_draft'

        states_texts = {
            '0_draft': _(u'La demande est en cours de création.'),
            '1_agep_validable': _(u'La demande doit être acceptée par l\'AGEPoly.'),
            '2_withdrawn': _(u'La somme est prête à être récupérée au secrétariat.'),
            '3_used': _(u'La somme a été retirée et doit maintenant être justifiée.'),
            '4_archived': _(u'La demande est archivée. Elle n\'est plus modifiable.'),
            '4_canceled': _(u'La demande a été annulée, potentiellement par refus.'),
        }

        states_links = {
            '0_draft': ['1_agep_validable', '4_canceled'],
            '1_agep_validable': ['2_withdrawn', '4_canceled'],
            '2_withdrawn': ['3_used', '4_canceled'],
            '3_used': ['4_archived'],
            '4_archived': [],
            '4_canceled': [],
        }

        list_quick_switch = {
            '0_draft': [('1_agep_validable', 'fa fa-question', _(u'Demander accord AGEPoly'))],
            '1_agep_validable': [('2_withdrawn', 'fa fa-check', _(u'Marquer comme retiré'))],
            '2_withdrawn': [('3_used', 'glyphicon glyphicon-remove-circle', _(u'Demander justification'))],
            '3_used': [('4_archived', 'glyphicon glyphicon-remove-circle', _(u'Archiver'))],
        }

        states_colors = {
            '0_draft': 'primary',
            '1_agep_validable': 'warning',
            '2_withdrawn': 'success',
            '3_used': 'danger',
            '4_archived': 'info',
            '4_canceled': 'default',
        }

        states_icons = {
            '0_draft': '',
            '1_agep_validable': '',
            '2_withdrawn': '',
            '3_used': '',
            '4_archived': '',
            '4_canceled': '',
        }

        forced_pos = {
            '0_draft': (0.1, 0.15),
            '1_agep_validable': (0.3, 0.15),
            '2_withdrawn': (0.5, 0.15),
            '3_used': (0.7, 0.15),
            '4_archived': (0.9, 0.15),
            '4_canceled': (0.9, 0.85),
        }

        states_default_filter = '0_draft,2_withdrawn,3_used'
        status_col_id = 3

        def build_form_withdrawn(request, obj):
            class FormWithdrawn(forms.Form):
                initial = obj.withdrawn_date if obj.withdrawn_date else now().date()
                withdrawn_date = forms.DateField(label=_('Date retrait banque'), help_text=_(u'La date de retrait à la banque'), required=True, initial=initial)

                def __init__(self, *args, **kwargs):

                    super(FormWithdrawn, self).__init__(*args, **kwargs)
                    self.fields['withdrawn_date'].widget.attrs = {'is_date': 'true'}

            return FormWithdrawn

        states_bonus_form = {
            '2_withdrawn': build_form_withdrawn
        }

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u"rcash"
        index_files = True

        fields = [
            'amount',
            'description',
            'name',
            'user',
        ]

    def may_switch_to(self, user, dest_state):
        if self.status[0] == '4' and not user.is_superuser:
            return False

        return super(_Withdrawal, self).may_switch_to(user, dest_state) and self.rights_can('EDIT', user)

    def can_switch_to(self, user, dest_state):
        if user.is_superuser:
            return (True, None)

        if self.status[0] == '4' and not user.is_superuser:
            return (False, _(u'Seul un super utilisateur peut sortir cet élément de l\'état archivé/annulé.'))

        if self.status in ['1_agep_validable', '2_withdrawn', '3_used'] and not self.rights_in_root_unit(user, 'SECRETARIAT'):
            return (False, _(u'Seules les secrétaires de l\'AGEPoly peuvent passer à l\'état suivant.'))

        if dest_state == '2_withdrawn' and not self.withdrawn_date:
            return (False, _(u'Il faut renseigner la date réelle du retrait avant de poursuivre.'))

        if not self.rights_can('EDIT', user):
            return (False, _('Pas les droits.'))

        return super(_Withdrawal, self).can_switch_to(user, dest_state)

    def rights_can_EDIT(self, user):
        if int(self.status[0]) > 3:
            return False

        # Seules les secrétaires peuvent modifier après le statut Brouillon (pour ajouter les dates de retrait et pièces comptables)
        if self.status != '0_draft' and not self.rights_in_root_unit(user, self.MetaRightsUnit.access):
            return False

        return super(_Withdrawal, self).rights_can_EDIT(user)

    def switch_status_signal(self, request, old_status, dest_status):

        s = super(_Withdrawal, self)

        if hasattr(s, 'switch_status_signal'):
            s.switch_status_signal(request, old_status, dest_status)

        if dest_status == '1_agep_validable':
            notify_people(request, '%s.validable' % (self.__class__.__name__,), 'accounting_validable', self, self.people_in_root_unit(self.MetaRightsUnit.access))

        elif dest_status == '2_withdrawn':
            if request.POST.get('withdrawn_date'):
                self.withdrawn_date = request.POST.get('withdrawn_date')
                self.save()

            unotify_people('%s.validable' % (self.__class__.__name__,), self)
            notify_people(request, '%s.withdrawn' % (self.__class__.__name__,), 'accounting_withdrawn', self, self.people_in_unit(self.costcenter.unit, access='TRESORERIE', no_parent=True))

        elif dest_status == '3_used':
            unotify_people('%s.withdrawn' % (self.__class__.__name__,), self)
            notify_people(request, '%s.used' % (self.__class__.__name__,), 'accounting_used', self, self.people_in_unit(self.costcenter.unit, access='TRESORERIE'))

        elif dest_status == '4_archived':
            unotify_people('%s.used' % (self.__class__.__name__,), self)

        elif dest_status == '4_canceled' and self.status != '0_draft':
            notify_people(request, '%s.canceled' % (self.__class__.__name__,), 'accounting_canceled', self, self.build_group_members_for_canedit())

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.costcenter)

    def genericFormExtraInit(self, form, current_user, *args, **kwargs):
        """Remove fields that should be edited by SECRETARIAT CDD only."""

        if not self.rights_in_root_unit(current_user, 'SECRETARIAT'):
            del form.fields['withdrawn_date']

    def rights_can_DISPLAY_LOG(self, user):

        # Don't disable logs if archived
        return super(_Withdrawal, self).rights_can_EDIT(user)


class LinkedInfo(models.Model):
    """Modèle pour les infos liées aux modèles de leur choix"""

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    linked_object = generic.GenericForeignKey('content_type', 'object_id')

    user_pk = models.PositiveIntegerField()
    first_name = models.CharField(_(u'Prénom'), max_length=50)
    last_name = models.CharField(_(u'Nom de famille'), max_length=50)
    address = models.TextField(_(u'Adresse'))
    phone = models.CharField(_(u'Numéro de téléphone'), max_length=20)
    bank = models.CharField(_(u'Nom de la banque'), max_length=128)
    iban_ccp = models.CharField(_(u'IBAN / CCP'), max_length=128)


class _ExpenseClaim(GenericModel, GenericTaggableObject, GenericAccountingStateModel, GenericStateModel, GenericModelWithFiles, GenericModelWithLines, AccountingYearLinked, CostCenterLinked, UnitEditableModel, GenericGroupsModel, GenericContactableModel, LinkedInfoModel, AccountingGroupModels, SearchableModel):
    """Modèle pour les notes de frais (NdF)"""

    class MetaRightsUnit(UnitEditableModel.MetaRightsUnit):
        access = ['TRESORERIE', 'SECRETARIAT']

    class MetaRights(UnitEditableModel.MetaRights):
        linked_unit_property = 'costcenter.unit'

    name = models.CharField(_(u'Titre de la note de frais'), max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nb_proofs = models.PositiveIntegerField(_(u'Nombre de justificatifs'), default=0)
    comment = models.TextField(_(u'Commentaire'), null=True, blank=True)

    class MetaData:
        list_display = [
            ('name', _('Titre')),
            ('costcenter', _(u'Centre de coûts')),
            ('get_fullname', _(u'Personne')),
            ('get_total_ht', _(u'Total (HT)')),
            ('get_total', _(u'Total (TTC)')),
            ('status', _('Statut')),
        ]

        details_display = list_display + [('nb_proofs', _(u'Nombre de justificatifs')), ('accounting_year', _(u'Année comptable')), ('comment', _(u'Commentaire'))]
        filter_fields = ('name', 'costcenter__name', 'costcenter__account_number', 'user__first_name', 'user__last_name', 'user__username')

        default_sort = "[0, 'desc']"  # Creation date (pk) descending
        trans_sort = {'get_fullname': 'user__first_name'}
        not_sortable_columns = ['get_total', 'get_total_ht']

        base_title = _(u'Notes de frais')
        list_title = _(u'Liste des notes de frais')
        files_title = _(u'Justificatifs')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-pencil-square-o'

        @staticmethod
        def extra_filter_for_list(request, current_unit, current_year, filtering):
            if current_unit.is_user_in_groupe(request.user, access=['TRESORERIE', 'SECRETARIAT']) or request.user.is_superuser:
                return lambda x: filtering(x)
            else:
                return lambda x: filtering(x).filter(user=request.user)

        has_unit = True

        menu_id = 'menu-compta-ndf'

        forced_widths = {
            '1': '350px',
        }

        help_list = _(u"""Les notes de frais permettent de se faire rembourser des frais avancés pour une unité.

Il est nécessaire de fournir les preuves d'achat et que celles-ci contiennent uniquement des choses qui doivent être remboursées.
Attention! Il faut faire une ligne par taux TVA par ticket. Par exemple, si certains achats à la Migros sont à 8% et d'autres à 0%, il faut les séparer en 2 lignes.""")

    class Meta:
        abstract = True

    class MetaEdit:
        files_title = _(u'Justificatifs')
        files_help = _(u'Justificatifs pour le remboursement de la note de frais.')

        all_users = True

    class MetaLines:
        lines_objects = [
            {
                'title': _(u'Lignes'),
                'class': 'accounting_tools.models.ExpenseClaimLine',
                'form': 'accounting_tools.forms2.ExpenseClaimLineForm',
                'related_name': 'lines',
                'field': 'expense_claim',
                'sortable': True,
                'tva_fields': ['tva'],
                'show_list': [
                    ('label', _(u'Titre')),
                    ('proof', _(u'Justificatif')),
                    ('account', _(u'Compte')),
                    ('value', _(u'Montant (HT)')),
                    ('get_tva', _(u'TVA')),
                    ('value_ttc', _(u'Montant (TTC)')),
                ]},
        ]

    class MetaGroups(GenericGroupsModel.MetaGroups):
        pass

    class MetaState(GenericAccountingStateModel.MetaState):
        pass

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u"NDF"
        index_files = True

        fields = [
            'name',
            'user',
            'comment',
            'get_total',
        ]

        linked_lines = {
            'lines': ['label', 'proof']
        }

    def __unicode__(self):
        return u"{} - {}".format(self.name, self.costcenter)

    def rights_can_EDIT(self, user):
        if not self.pk or (self.get_creator() == user and self.status[0] == '0'):
            return True

        return super(_ExpenseClaim, self).rights_can_EDIT(user)

    def rights_can_LIST(self, user):
        return True  # Tout le monde peut lister les notes de frais de n'importe quelle unité (à noter qu'il y a un sous filtre qui affiche que les NDF que l'user peut voir dans la liste)

    def genericFormExtraClean(self, data, form):
        if 'user' in data and not data['user'].is_profile_ok():
            form._errors["user"] = form.error_class([_(u"Le profil de cet utilisateur doit d'abord être completé.")])  # Until Django 1.6
            # form.add_error("user", _(u"Le profil de cet utilisateur doit d'abord être completé."))  # From Django 1.7

        if 'user' in data and data['user'] != form.truffe_request.user and not self.rights_in_linked_unit(form.truffe_request.user, self.MetaRightsUnit.access) and not form.truffe_request.user.is_superuser:
            form._errors["user"] = form.error_class([_(u"Il faut plus de droits pour pouvoir faire une note de frais pour quelqu'un d'autre.")])  # Until Django 1.6
            # form.add_error("user", _(u"Il faut plus de droits pour pouvoir faire une note de frais pour quelqu'un d'autre."))  # From Django 1.7

    def get_lines(self):
        return self.lines.order_by('order')

    def get_total(self):
        return sum([line.value_ttc for line in self.get_lines()])

    def get_total_ht(self):
        return sum([line.value for line in self.get_lines()])

    def is_unit_validator(self, user):
        """Check if user is a validator for the step '1_unit_validable'."""
        return self.rights_in_linked_unit(user, self.MetaRightsUnit.access)


class ExpenseClaimLine(ModelUsedAsLine):

    expense_claim = models.ForeignKey('ExpenseClaim', related_name="lines")

    label = models.CharField(_(u'Concerne'), max_length=255)
    proof = models.CharField(_(u'Justificatif'), max_length=255, blank=True)

    account = models.ForeignKey('accounting_core.Account', verbose_name=_('Compte'))
    value = models.DecimalField(_(u'Montant (HT)'), max_digits=20, decimal_places=2)
    tva = models.DecimalField(_(u'TVA'), max_digits=20, decimal_places=2)
    value_ttc = models.DecimalField(_(u'Montant (TTC)'), max_digits=20, decimal_places=2)

    def __unicode__(self):
        return u'{}: {} + {}% == {}'.format(self.label, self.value, self.tva, self.value_ttc)

    def get_tva(self):
        from accounting_core.models import TVA
        return TVA.tva_format(self.tva)

    def display_amount(self):
        return u'{} + {}% == {}'.format(self.value, self.tva, self.value_ttc)


class _CashBook(GenericModel, GenericTaggableObject, GenericAccountingStateModel, GenericStateModel, GenericModelWithFiles, GenericModelWithLines, AccountingYearLinked, CostCenterLinked, UnitEditableModel, GenericGroupsModel, GenericContactableModel, LinkedInfoModel, AccountingGroupModels, SearchableModel):
    """Modèle pour les journaux de caisse (JdC)"""

    class MetaRightsUnit(UnitEditableModel.MetaRightsUnit):
        access = ['TRESORERIE', 'SECRETARIAT']

    class MetaRights(UnitEditableModel.MetaRights):
        linked_unit_property = 'costcenter.unit'

    name = models.CharField(_(u'Titre du journal de caisse'), max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nb_proofs = models.PositiveIntegerField(_(u'Nombre de justificatifs'), default=0)
    comment = models.TextField(_(u'Commentaire'), null=True, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    proving_object = generic.GenericForeignKey('content_type', 'object_id')

    class MetaData:
        list_display = [
            ('name', _('Titre')),
            ('costcenter', _(u'Centre de coûts')),
            ('get_fullname', _(u'Personne')),
            ('get_total_ht', _(u'Total (HT)')),
            ('get_total', _(u'Total (TTC)')),
            ('status', _('Statut')),
        ]

        details_display = list_display + [('nb_proofs', _(u'Nombre de justificatifs')), ('accounting_year', _(u'Année comptable')), ('comment', _(u'Commentaire'))]
        filter_fields = ('name', 'costcenter__name', 'costcenter__account_number', 'user__first_name', 'user__last_name', 'user__username')

        default_sort = "[0, 'desc']"  # Creation date (pk) descending
        trans_sort = {'get_fullname': 'user__first_name'}
        not_sortable_columns = ['get_total', 'get_total_ht']

        base_title = _(u'Journaux de caisse')
        list_title = _(u'Liste des journaux de caisse')
        files_title = _(u'Justificatifs')
        base_icon = 'fa fa-list'
        elem_icon = 'fa fa-pencil-square-o'

        @staticmethod
        def extra_args_for_edit(request, current_unit, current_year):
            return {'CS_account_number': settings.CS_ACCOUNT_NUMBER}

        has_unit = True

        menu_id = 'menu-compta-jdc'

        help_list = _(u"""Les journaux de caisse servent à justifier des dépenses et des recettes liées à des versements à la banque ou des retraits cash.

Il est nécessaire de fournir les preuves d'achat et que celles-ci contiennent uniquement des choses qui doivent être remboursées.
Attention! Il faut faire une ligne par taux TVA par ticket. Par exemple, si certains achats à la Migros sont à 8% et d'autres à 0%, il faut les séparer en 2 lignes.""")

    class Meta:
        abstract = True

    class MetaEdit:
        files_title = _(u'Justificatifs')
        files_help = _(u'Justificatifs liés aux lignes du journal de caisse.')

        all_users = True

    class MetaLines:
        lines_objects = [
            {
                'title': _(u'Lignes'),
                'class': 'accounting_tools.models.CashBookLine',
                'form': 'accounting_tools.forms2.CashBookLineForm',
                'related_name': 'lines',
                'field': 'cashbook',
                'sortable': True,
                'tva_fields': ['tva'],
                'date_fields': ['date'],
                'show_list': [
                    ('date', _(u'Date')),
                    ('get_helper_display', _(u'Type')),
                    ('label', _(u'Titre')),
                    ('proof', _(u'Justificatif')),
                    ('account', _(u'Compte')),
                    ('value', _(u'Montant (HT)')),
                    ('get_tva', _(u'TVA')),
                    ('value_ttc', _(u'Montant (TTC)')),
                ]},
        ]

    class MetaGroups(GenericGroupsModel.MetaGroups):
        pass

    class MetaState(GenericAccountingStateModel.MetaState):

        def build_form_archive(request, obj):
            class FormArchive(forms.Form):
                archive_proving_obj = forms.BooleanField(label=_(u'Archiver le retrait cash lié?'), initial=True, required=False)
            return FormArchive if obj.proving_object else None

        states_bonus_form = {
            '4_archived': build_form_archive
        }

    class MetaSearch(SearchableModel.MetaSearch):

        extra_text = u"JDC"
        index_files = True

        fields = [
            'name',
            'user',
            'comment',
            'get_total',
        ]

        linked_lines = {
            'lines': ['label', 'proof', 'amount']
        }

    def __unicode__(self):
        return u"{} - {}".format(self.name, self.costcenter)

    def genericFormExtraClean(self, data, form):
        if 'withdrawal' in data.keys() and data['withdrawal']:
            if 'user' not in data or 'costcenter' not in data:
                client.captureMessage('Withdrawal linked to Cashbook is missing mandatory data (user / costcenter)!\n{}'.format(data))

            if data['withdrawal'].user != data.get('user', '') or data['withdrawal'].costcenter != data.get('costcenter', ''):
                raise forms.ValidationError(_(u'L\'utilisateur responsable et/ou le centre de coûts ne correspondent pas au retrait cash lié.'))

            data['object_id'] = data['withdrawal'].pk
            data['content_type'] = ContentType.objects.get(app_label=data['withdrawal']._meta.app_label, model=data['withdrawal']._meta.model_name)
            del data['withdrawal']
        else:
            data['object_id'] = None
            data['content_type'] = None

        if 'user' in data and not data['user'].is_profile_ok():
            form._errors["user"] = form.error_class([_(u"Le profil de cet utilisateur doit d'abord être completé.")])  # Until Django 1.6
            # form.add_error("user", _(u"Le profil de cet utilisateur doit d'abord être completé."))  # From Django 1.7

        if 'user' in data and data['user'] != form.truffe_request.user and not self.rights_in_linked_unit(form.truffe_request.user, self.MetaRightsUnit.access) and not form.truffe_request.user.is_superuser:
            form._errors["user"] = form.error_class([_(u"Il faut plus de droits pour pouvoir faire une note de frais pour quelqu'un d'autre.")])  # Until Django 1.6
            # form.add_error("user", _(u"Il faut plus de droits pour pouvoir faire une note de frais pour quelqu'un d'autre."))  # From Django 1.7

    def genericFormExtraInit(self, form, current_user, *args, **kwargs):
        """Set related object correctly."""
        from accounting_tools.models import Withdrawal

        form.fields['withdrawal'] = forms.ModelChoiceField(queryset=Withdrawal.objects.order_by('-pk'), initial=self.proving_object, required=False, label=_(u'Retrait cash lié'))

        for field in ['content_type', 'object_id']:
            del form.fields[field]

    def get_lines(self):
        return self.lines.order_by('order')

    def get_total(self):
        return sum([line.get_line_delta() for line in self.get_lines()])

    def get_total_ht(self):
        return sum([line.get_line_delta_ht() for line in self.get_lines()])

    def total_incomes(self):
        return sum([line.input_amount() for line in self.get_lines()])

    def total_outcomes(self):
        return sum([line.output_amount() for line in self.get_lines()])

    def is_unit_validator(self, user):
        """Check if user is a validator for the step '1_unit_validable'."""
        return self.rights_in_linked_unit(user, self.MetaRightsUnit.access)


class CashBookLine(ModelUsedAsLine):

    HELPER_TYPE = (
        ('0_withdraw', _(u'J\'ai fait un retrait cash : ')),
        ('1_deposit', _(u'J\'ai fait un versement à la banque : ')),
        ('2_sell', _(u'J\'ai vendu quelque chose : ')),
        ('3_invoice', _(u'J\'ai payé une facture avec la caisse : ')),
        ('4_buy', _(u'J\'ai acheté quelque chose avec la caisse : ')),
        ('5_reimburse', _(u'J\'ai remboursé quelqu\'un avec la caisse : ')),
        ('6_input', _(u'Je fais un Crédit manuel : ')),
        ('7_output', _(u'Je fais un Débit manuel : ')),
    )

    cashbook = models.ForeignKey('CashBook', related_name="lines")

    date = models.DateField(_(u'Date'))
    helper = models.CharField(max_length=15, choices=HELPER_TYPE)
    label = models.CharField(_(u'Concerne'), max_length=255)
    proof = models.CharField(_(u'Justificatif'), max_length=255, blank=True)

    account = models.ForeignKey('accounting_core.Account', verbose_name=_('Compte'))
    value = models.DecimalField(_(u'Montant (HT)'), max_digits=20, decimal_places=2)
    tva = models.DecimalField(_(u'TVA'), max_digits=20, decimal_places=2)
    value_ttc = models.DecimalField(_(u'Montant (TTC)'), max_digits=20, decimal_places=2)

    def __unicode__(self):
        return u'{}: {} + {}% == {}'.format(self.label, self.value, self.tva, self.value_ttc)

    def get_tva(self):
        from accounting_core.models import TVA
        return TVA.tva_format(self.tva)

    def display_amount(self):
        return u'{} + {}% == {}'.format(self.value, self.tva, self.value_ttc)

    def input_amount(self):
        return self.value_ttc if self.is_input else 0

    def output_amount(self):
        return self.value_ttc if self.is_output else 0

    def get_line_delta(self):
        return self.input_amount() - self.output_amount()

    @property
    def is_input(self):
        return self.helper[0] in ['0', '2', '6']

    @property
    def is_output(self):
        return self.helper[0] not in ['0', '2', '6']

    def input_amount_ht(self):
        return self.value if self.is_input else 0

    def output_amount_ht(self):
        return self.value if self.is_output else 0

    def get_line_delta_ht(self):
        return self.input_amount_ht() - self.output_amount_ht()

    def sub_total(self):
        previous_lines = list(self.cashbook.lines.filter(order__lte=self.order))  # including self
        return sum(map(lambda line: line.get_line_delta(), previous_lines))
