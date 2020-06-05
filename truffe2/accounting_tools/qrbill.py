# -*-coding:utf-8 -*
# This file should be removed when switching to python3
from __future__ import absolute_import
import re
from datetime import date
from decimal import Decimal
from io import BytesIO

import qrcode
import qrcode.image.svg
import svgwrite
from iso3166 import countries
from stdnum import iban, iso11649
from stdnum.ch import esr

IBAN_ALLOWED_COUNTRIES = [u'CH', u'LI']
QR_IID = {u"start": 30000, u"end": 31999}
AMOUNT_REGEX = u'^\d{1,9}\.\d{2}$'
DATE_REGEX = u'(\d{4})-(\d{2})-(\d{2})'
MM_TO_UU = 3.543307

# Annex D: Multilingual headings
LABELS = {
    u'Payment part': {u'de': u'Zahlteil', u'fr': u'Section paiement', u'it': u'Sezione pagamento'},
    u'Account / Payable to': {
        u'de': u'Konto / Zahlbar an',
        u'fr': u'Compte / Payable à',
        u'it': u'Conto / Pagabile a',
    },
    u'Reference': {u'de': u'Referenz', u'fr': u'Référence', u'it': u'Riferimento'},
    u'Additional information': {
        u'de': u'Zusätzliche Informationen',
        u'fr': u'Informations supplémentaires',
        u'it': u'Informazioni supplementari',
    },
    u'Currency': {u'de': u'Währung', u'fr': u'Monnaie', u'it': u'Valuta'},
    u'Amount': {u'de': u'Betrag', u'fr': u'Montant', u'it': u'Importo'},
    u'Receipt': {u'de': u'Empfangsschein', u'fr': u'Récépissé', u'it': u'Ricevuta'},
    u'Acceptance point': {u'de': u'Annahmestelle', u'fr': u'Point de dépôt', u'it': u'Punto di accettazione'},
    u'Separate before paying in': {
        u'de': u'Vor der Einzahlung abzutrennen',
        u'fr': u'A détacher avant le versement',
        u'it': u'Da staccare prima del versamento',
    },
    u'Payable by': {u'de': u'Zahlbar durch', u'fr': u'Payable par', u'it': u'Pagabile da'},
    u'Payable by (name/address)': {
        u'de': u'Zahlbar durch (Name/Adresse)',
        u'fr': u'Payable par (nom/adresse)',
        u'it': u'Pagabile da (nome/indirizzo)',
    },
    # The extra ending space allows to differentiate from the other 'Payable by' above.
    u'Payable by ': {u'de': u'Zahlbar bis', u'fr': u'Payable jusqu’au', u'it': u'Pagabile fino al'},
    u'In favour of': {u'de': u'Zugunsten', u'fr': u'En faveur de', u'it': u'A favore di'},
}


class Address(object):
    def __init__(self, **_3to2kwargs):
        if 'country' in _3to2kwargs: country = _3to2kwargs['country']; del _3to2kwargs['country']
        else: country = None
        if 'city' in _3to2kwargs: city = _3to2kwargs['city']; del _3to2kwargs['city']
        else: city = None
        if 'pcode' in _3to2kwargs: pcode = _3to2kwargs['pcode']; del _3to2kwargs['pcode']
        else: pcode = None
        if 'house_num' in _3to2kwargs: house_num = _3to2kwargs['house_num']; del _3to2kwargs['house_num']
        else: house_num = None
        if 'street' in _3to2kwargs: street = _3to2kwargs['street']; del _3to2kwargs['street']
        else: street = None
        if 'name' in _3to2kwargs: name = _3to2kwargs['name']; del _3to2kwargs['name']
        else: name = None
        if 'line1' in _3to2kwargs: line1 = _3to2kwargs['line1']; del _3to2kwargs['line1']
        else: line1 = None
        if 'line2' in _3to2kwargs: line2 = _3to2kwargs['line2']; del _3to2kwargs['line2']
        else: line2 = None

        self.name = (name or u'').strip()
        if not (1 <= len(self.name) <= 70):
            raise ValueError(u"An address name should have between 1 and 70 characters.")

        if line1 is not None:
            self.line1 = (line1 or u'').strip()
            if not (0 <= len(self.line1) <= 70):
                raise ValueError(u"An address line should have between 0 and 70 characters.")
            self.line2 = (line2 or u'').strip()
            if not (0 <= len(self.line2) <= 70):
                raise ValueError(u"An address line2 should have between 0 and 70 characters.")
            self.combined = True

        else:
            self.street = (street or u'').strip()
            if len(self.street) > 70:
                raise ValueError(u"A street cannot have more than 70 characters.")
            self.house_num = (house_num or u'').strip()
            if len(self.house_num) > 16:
                raise ValueError(u"A house number cannot have more than 16 characters.")
            self.pcode = (pcode or u'').strip()
            if not self.pcode:
                raise ValueError(u"Postal code is mandatory")
            elif len(self.pcode) > 16:
                raise ValueError(u"A postal code cannot have more than 16 characters.")
            self.city = (city or u'').strip()
            if not self.city:
                raise ValueError(u"City is mandatory")
            elif len(self.city) > 35:
                raise ValueError(u"A city cannot have more than 35 characters.")
            country = (country or u'').strip()
            # allow users to write the country as if used in an address in the local language
            if not country or country.lower() in [u'schweiz', u'suisse', u'svizzera', u'svizra']:
                country = u'CH'
            if country.lower() in [u'fürstentum liechtenstein']:
                country = u'LI'
            try:
                self.country = countries.get(country).alpha2
            except KeyError:
                raise ValueError(u"The country code '%s' is not valid" % country)
            self.country = countries.get(country).alpha2
            self.combined = False

    def data_list(self):
        u"""Return address values as a list, appropriate for qr generation."""
        # 'S': structured address
        if self.combined:
            return [
                u'K', self.name, self.line1, self.line2, '', '', ''
            ]
        else:
            return [
                u'S', self.name, self.street, self.house_num, self.pcode,
                self.city, self.country
            ]

    def as_paragraph(self):
        if self.combined:
            lines = [self.name, self.line1, self.line2]
        else:
            lines = [self.name, u"%s-%s %s" % (self.country, self.pcode, self.city)]
            if self.street:
                if self.house_num:
                    lines.insert(1, u" ".join([self.street, self.house_num]))
                else:
                    lines.insert(1, self.street)
        return lines


class QRBill(object):
    u"""This class represents a Swiss QR Bill."""
    # Header fields
    qr_type = u'SPC'  # Swiss Payments Code
    version = u'0200'
    coding = 1  # Latin character set
    allowed_currencies = (u'CHF', u'EUR')
    # QR reference, Creditor Reference (ISO 11649), without reference
    reference_types = (u'QRR', u'SCOR', u'NON')

    def __init__(
            self, account=None, creditor=None, final_creditor=None, amount=None,
            currency=u'CHF', due_date=None, debtor=None, ref_number=None, extra_infos=u'',
            language=u'en', top_line=False, extra_auto_infos=None):
        # Account (IBAN) validation
        if not account:
            raise ValueError(u"The account parameter is mandatory")
        if not iban.is_valid(account):
            raise ValueError(u"Sorry, the IBAN is not valid")
        self.account = iban.validate(account)
        if self.account[:2] not in IBAN_ALLOWED_COUNTRIES:
            raise ValueError(u"IBAN must start with: %s" % u", ".join(IBAN_ALLOWED_COUNTRIES))
        iban_iid = int(self.account[4:9])
        if QR_IID[u"start"] <= iban_iid <= QR_IID[u"end"]:
            self.account_is_qriban = True
        else:
            self.account_is_qriban = False

        if amount is not None:
            if isinstance(amount, Decimal):
                amount = unicode(amount)
            elif not isinstance(amount, unicode):
                raise ValueError(u"Amount can only be specified as str or Decimal.")
            # remove commonly used thousands separators
            amount = amount.replace(u"'", u"").strip()
            # people often don't add .00 for amounts without cents/rappen
            if u"." not in amount:
                amount = amount + u".00"
            # support lazy people who write 12.1 instead of 12.10
            if amount[-2] == u'.':
                amount = amount + u'0'
            # strip leading zeros
            amount = amount.lstrip(u"0")
            # some people tend to strip the leading zero on amounts below 1 CHF/EUR
            # and with removing leading zeros, we would have removed the zero before
            # the decimal delimiter anyway
            if amount[0] == u".":
                amount = u"0" + amount
            m = re.match(AMOUNT_REGEX, amount)
            if not m:
                raise ValueError(
                    u"If provided, the amount must match the pattern '###.##'"
                    u" and cannot be larger than 999'999'999.99"
                )
        self.amount = amount
        if currency not in self.allowed_currencies:
            raise ValueError(u"Currency can only contain: %s" % u", ".join(self.allowed_currencies))
        self.currency = currency
        if due_date:
            m = re.match(DATE_REGEX, due_date)
            if not m:
                raise ValueError(u"The date must match the pattern 'YYYY-MM-DD'")
            due_date = date(*[int(g)for g in m.groups()])
        self.due_date = due_date
        if not creditor:
            raise ValueError(u"Creditor information is mandatory")
        try:
            self.creditor = Address(**creditor)
        except ValueError as err:
            raise ValueError(u"The creditor address is invalid: %s" % err)
        if final_creditor is not None:
            # The standard says ultimate creditor is reserved for future use.
            # The online validator does not properly validate QR-codes where
            # this is set, saying it must not (yet) be used.
            raise ValueError(u"final creditor is reserved for future use, must not be used")
        else:
            self.final_creditor = final_creditor
        if debtor is not None:
            try:
                self.debtor = Address(**debtor)
            except ValueError as err:
                raise ValueError(u"The debtor address is invalid: %s" % err)
        else:
            self.debtor = debtor

        if not ref_number:
            self.ref_type = u'NON'
            self.ref_number = None
        elif ref_number.strip()[:2].upper() == u"RF":
            if iso11649.is_valid(ref_number):
                self.ref_type = u'SCOR'
                self.ref_number = iso11649.validate(ref_number)
            else:
                raise ValueError(u"The reference number is invalid")
        elif esr.is_valid(ref_number):
            self.ref_type = u'QRR'
            self.ref_number = esr.format(ref_number).replace(u" ", u"")
        else:
            raise ValueError(u"The reference number is invalid")

        # A QRR reference number must only be used with a QR-IBAN and
        # with a QR-IBAN, a QRR reference number must be used
        if self.account_is_qriban:
            if self.ref_type != u'QRR':
                raise ValueError(u"A QR-IBAN requires a QRR reference number")
        else:
            if self.ref_type == u'QRR':
                raise ValueError(u"A QRR reference number is only allowed for a QR-IBAN")

        self.extra_infos = u''
        if extra_infos and len(extra_infos) > 140:
            raise ValueError(u"Additional information cannot contain more than 140 characters")
        self.extra_infos = extra_infos

        if language not in [u'en', u'de', u'fr', u'it']:
            raise ValueError(u"Language should be 'en', 'de', 'fr', or 'it'")
        self.language = language
        self.top_line = top_line

        self.extra_auto_infos = u''
        if extra_auto_infos and len(extra_auto_infos) > 140:
            raise ValueError(u"Additional information cannot contain more than 140 characters")
        self.extra_auto_infos = extra_auto_infos

    def qr_data(self):
        u"""Return data to be encoded in the QR code."""
        values = [self.qr_type or u'', self.version or u'', self.coding or u'', self.account or u'']
        values.extend(self.creditor.data_list())
        values.extend(self.final_creditor.data_list() if self.final_creditor else [u''] * 7)
        values.extend([self.amount or u'', self.currency or u''])
        values.extend(self.debtor.data_list() if self.debtor else [u''] * 7)
        values.extend([self.ref_type or u'', self.ref_number or u'', self.extra_infos or u'', u'EPD', self.extra_auto_infos])
        return u"\r\n".join([unicode(v) for v in values])

    def qr_image(self):
        factory = qrcode.image.svg.SvgPathImage
        return qrcode.make(
            self.qr_data(),
            image_factory=factory,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )

    def draw_swiss_cross(self, dwg, qr_width):
        group = dwg.add(dwg.g(id=u"swiss-cross"))
        group.add(
            dwg.polygon(points=[
                (18.3, 0.7), (1.6, 0.7), (0.7, 0.7), (0.7, 1.6), (0.7, 18.3), (0.7, 19.1),
                (1.6, 19.1), (18.3, 19.1), (19.1, 19.1), (19.1, 18.3), (19.1, 1.6), (19.1, 0.7)
            ])
        )
        group.add(
            dwg.rect(insert=(8.3, 4), size=(3.3, 11), fill=u'white')
        )
        group.add(
            dwg.rect(insert=(4.4, 7.9), size=(11, 3.3), fill=u'white')
        )
        group.add(
            dwg.polygon(points=[
                (0.7, 1.6), (0.7, 18.3), (0.7, 19.1), (1.6, 19.1), (18.3, 19.1), (19.1, 19.1),
                (19.1, 18.3), (19.1, 1.6), (19.1, 0.7), (18.3, 0.7), (1.6, 0.7), (0.7, 0.7)],
                fill=u'none', stroke=u'white', stroke_width=1.4357,
            )
        )
        x = 250 + (qr_width * 0.52)
        y = 58 + (qr_width * 0.52)
        group.translate(tx=x, ty=y)

    def draw_blank_rect(self, dwg, x, y, width, height):
        u"""Draw a empty blank rect with corners (e.g. amount, debtor)"""
        stroke_info = {u'stroke': u'black', u'stroke_width': u'0.7mm', u'stroke_linecap': u'square'}
        grp = dwg.add(dwg.g())
        grp.add(dwg.line((x, y), (x, add_mm(y, u'2mm')), **stroke_info))
        grp.add(dwg.line((x, y), (add_mm(x, u'3mm'), y), **stroke_info))
        grp.add(dwg.line((x, add_mm(y, height)), (x, add_mm(y, height, u'-2mm')), **stroke_info))
        grp.add(dwg.line((x, add_mm(y, height)), (add_mm(x, u'3mm'), add_mm(y, height)), **stroke_info))
        grp.add(dwg.line((add_mm(x, width, u'-3mm'), y), (add_mm(x, width), y), **stroke_info))
        grp.add(dwg.line((add_mm(x, width), y), (add_mm(x, width), add_mm(y, u'2mm')), **stroke_info))
        grp.add(dwg.line(
            (add_mm(x, width, u'-3mm'), add_mm(y, height)), (add_mm(x, width), add_mm(y, height)),
            **stroke_info
        ))
        grp.add(dwg.line(
            (add_mm(x, width), add_mm(y, height)), (add_mm(x, width), add_mm(y, height, u'-2mm')),
            **stroke_info
        ))

    def label(self, txt):
        return txt if self.language == u'en' else LABELS[txt][self.language]

    def as_svg(self, file_name, file_obj=None):
        bill_height = u'105mm'
        receipt_width = u'62mm'
        payment_width = u'148mm'
        margin = u'5mm'
        payment_left = add_mm(receipt_width, margin)
        payment_detail_left = add_mm(payment_left, u'70mm')
        title_font_info = {u'font_size': 11, u'font_family': u'helvetica', u'font_weight': u'bold'}
        font_info = {u'font_size': 10, u'font_family': u'helvetica'}
        head_font_info = {u'font_size': 8, u'font_family': u'helvetica', u'font_weight': u'bold'}

        dwg = svgwrite.Drawing(
            size=(add_mm(receipt_width, payment_width), bill_height),  # A4 width, A6 height.
            filename=file_name,
        )
        dwg.add(dwg.rect(insert=(0, 0), size=(u'100%', u'100%'), fill=u'white'))  # Force white background

        # Receipt
        y_pos = 15
        line_space = 3.5
        dwg.add(dwg.text(self.label(u"Receipt"), (margin, u'10mm'), **title_font_info))
        dwg.add(dwg.text(self.label(u"Account / Payable to"), (margin, u'%smm' % y_pos), **head_font_info))
        y_pos += line_space
        dwg.add(dwg.text(
            iban.format(self.account), (margin, u'%smm' % y_pos), **font_info
        ))
        y_pos += line_space
        for line_text in self.creditor.as_paragraph():
            dwg.add(dwg.text(line_text, (margin, u'%smm' % y_pos), **font_info))
            y_pos += line_space

        if self.ref_number:
            y_pos += 1
            dwg.add(dwg.text(self.label(u"Reference"), (margin, u'%smm' % y_pos), **head_font_info))
            y_pos += line_space
            dwg.add(dwg.text(format_ref_number(self), (margin, u'%smm' % y_pos), **font_info))
            y_pos += line_space

        y_pos += 1
        dwg.add(dwg.text(
            self.label(u"Payable by") if self.debtor else self.label(u"Payable by (name/address)"),
            (margin, u'%smm' % y_pos), **head_font_info
        ))
        y_pos += line_space
        if self.debtor:
            for line_text in self.debtor.as_paragraph():
                dwg.add(dwg.text(line_text, (margin, u'%smm' % y_pos), **font_info))
                y_pos += line_space
        else:
            self.draw_blank_rect(
                dwg, x=margin, y=u'%smm' % y_pos,
                width=u'52mm', height=u'25mm'
            )
            y_pos += 28

        dwg.add(dwg.text(self.label(u"Currency"), (margin, u'80mm'), **head_font_info))
        dwg.add(dwg.text(self.label(u"Amount"), (add_mm(margin, u'12mm'), u'80mm'), **head_font_info))
        dwg.add(dwg.text(self.currency, (margin, u'85mm'), **font_info))
        if self.amount:
            dwg.add(dwg.text(format_amount(self.amount), (add_mm(margin, u'12mm'), u'85mm'), **font_info))
        else:
            self.draw_blank_rect(
                dwg, x=add_mm(margin, u'25mm'), y=u'77mm',
                width=u'27mm', height=u'11mm'
            )

        # Right-aligned
        dwg.add(dwg.text(
            self.label(u"Acceptance point"), (add_mm(receipt_width, u'-' + margin), u'91mm'),
            text_anchor=u'end', **head_font_info
        ))

        # Top separation line
        if self.top_line:
            dwg.add(dwg.line(
                start=(0, 0), end=(u'100%', 0),
                stroke=u'black', stroke_dasharray=u'2 2'
            ))
        # Separation line between receipt and payment parts
        dwg.add(dwg.line(
            start=(receipt_width, 0), end=(receipt_width, bill_height),
            stroke=u'black', stroke_dasharray=u'2 2'
        ))
        dwg.add(dwg.text(
            u"✂", insert=(add_mm(receipt_width, u'-1.5mm'), 40),
            font_size=16, font_family=u'helvetica', rotate=[90]
        ))

        # Payment part
        dwg.add(dwg.text(self.label(u"Payment part"), (payment_left, u'10mm'), **title_font_info))

        # Get QR code SVG from qrcode lib, read it and redraw path in svgwrite drawing.
        buff = BytesIO()
        im = self.qr_image()
        im.save(buff)
        m = re.search(ur'<path [^>]*>', buff.getvalue().decode())
        if not m:
            raise Exception(u"Unable to extract path data from the QR code SVG image")
        m = re.search(ur' d=\"([^\"]*)\"', m.group())
        if not m:
            raise Exception(u"Unable to extract path d attributes from the SVG QR code source")
        path_data = m.groups()[0]
        path = dwg.path(
            d=path_data,
            style=u"fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none",
        )
        path.translate(tx=250, ty=60)
        # Limit scaling to some max dimensions
        scale_factor = 3 - (max(im.width - 60, 0) * 0.05)
        path.scale(sx=scale_factor, sy=scale_factor)
        dwg.add(path)

        self.draw_swiss_cross(dwg, im.width * scale_factor)

        dwg.add(dwg.text(self.label(u"Currency"), (payment_left, u'80mm'), **head_font_info))
        dwg.add(dwg.text(self.label(u"Amount"), (add_mm(payment_left, u'12mm'), u'80mm'), **head_font_info))
        dwg.add(dwg.text(self.currency, (payment_left, u'85mm'), **font_info))
        if self.amount:
            dwg.add(dwg.text(format_amount(self.amount), (add_mm(payment_left, u'12mm'), u'85mm'), **font_info))
        else:
            self.draw_blank_rect(
                dwg, x=add_mm(receipt_width, margin, u'12mm'), y=u'83mm',
                width=u'40mm', height=u'15mm'
            )

        # Right side of the bill
        y_pos = 10
        line_space = 3.5

        def add_header(dwg, payment_detail_left, y_pos, text):
            y_pos += 1
            dwg.add(dwg.text(text, (payment_detail_left, u'%smm' % y_pos), **head_font_info))
            y_pos += line_space
            return y_pos

        y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Account / Payable to"))
        dwg.add(dwg.text(
            iban.format(self.account), (payment_detail_left, u'%smm' % y_pos), **font_info
        ))
        y_pos += line_space

        for line_text in self.creditor.as_paragraph():
            dwg.add(dwg.text(line_text, (payment_detail_left, u'%smm' % y_pos), **font_info))
            y_pos += line_space

        if self.ref_number:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Reference"))
            dwg.add(dwg.text(
                format_ref_number(self), (payment_detail_left, u'%smm' % y_pos), **font_info
            ))
            y_pos += line_space

        if self.extra_infos:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Additional information"))
            if u'##' in self.extra_infos:
                extra_infos = self.extra_infos.split(u'##')
                extra_infos[1] = u'##' + extra_infos[1]
            else:
                extra_infos = [self.extra_infos]
            # TODO: handle line breaks for long infos (mandatory 5mm margin)
            for info in wrap_infos(extra_infos):
                dwg.add(dwg.text(info, (payment_detail_left, u'%smm' % y_pos), **font_info))
                y_pos += line_space

        if self.debtor:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Payable by"))
            for line_text in self.debtor.as_paragraph():
                dwg.add(dwg.text(line_text, (payment_detail_left, u'%smm' % y_pos), **font_info))
                y_pos += line_space
        else:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Payable by (name/address)"))
            # The specs recomment at least 2.5 x 6.5 cm
            self.draw_blank_rect(
                dwg, x=payment_detail_left, y=u'%smm' % y_pos,
                width=u'65mm', height=u'25mm'
            )
            y_pos += 28

        if self.final_creditor:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"In favor of"))
            for line_text in self.final_creditor.as_paragraph():
                dwg.add(dwg.text(line_text, (payment_detail_left, u'%smm' % y_pos), **font_info))
                y_pos += line_space

        if self.due_date:
            y_pos = add_header(dwg, payment_detail_left, y_pos, self.label(u"Payable by "))
            dwg.add(dwg.text(
                format_date(self.due_date), (payment_detail_left, u'%smm' % y_pos), **font_info
            ))
            y_pos += line_space

        if file_obj:
            dwg.write(file_obj)
        else:
            dwg.save()

def add_mm(*mms):
    u"""Utility to allow additions of '23mm'-type strings."""
    return u'%smm' % unicode(sum(float(mm[:-2]) for mm in mms))


def format_ref_number(bill):
    if not bill.ref_number:
        return u''
    num = bill.ref_number
    if bill.ref_type == u"QRR":
        return esr.format(num)
    elif bill.ref_type == u"SCOR":
        return iso11649.format(num)
    else:
        return num


def format_date(date_):
    if not date_:
        return u''
    return date_.strftime(u'%d.%m.%Y')


def format_amount(amount_):
    return u'{:,.2f}'.format(float(amount_)).replace(u",", u" ")


def wrap_infos(infos):
    for text in infos:
        while(text):
            yield text[:42]
            text = text[42:]
