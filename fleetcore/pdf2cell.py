# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os
import re
import sys

from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from pdfminer.converter import (
    enc,
    TextConverter,
)
from pdfminer.layout import *
from pdfminer.pdfinterp import (
    PDFResourceManager,
    process_pdf,
)
from pdfminer.pdfparser import (
    PDFSyntaxError,
)
from pdfminer.converter import PDFPageAggregator, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

(PHONE_NUMBER, USER, PLAN, MONTHLY_PRICE, SERVICES, REFUNDS,
 INCLUDED_MIN,
 EXCEEDED_STABLISHING_MIN, EXCEEDED_STABLISHING_MIN_PRICE,
 EXCEEDED_MIN, EXCEEDED_MIN_PRICE,
 NDL_MIN, NDL_PRICE, IDL_MIN, IDL_PRICE,
 SMS, SMS_PRICE,
 OTHER_PRICE, TOTAL_PRICE) = range(19)

PHONE_ROW_RE = re.compile(r'\s*(\d+,\d{2})\s*')
PHONE_TOKEN = '-'
PERCENT_RE = '(\d+(?:\.\d+){0,1})%'
PRICE_RE = '((?:\d+\.){0,1}\d+,\d+)'
TAX_FINANC_RE = re.compile(
    r'Cargo (\d+(?:\.\d+){0,1})% financ ENARD Ley 26\.573/09\s+(\d+,\d+)',
    re.IGNORECASE)
TAX_INTERNAL_RE = re.compile(
    r'Impuesto Interno\s*(\d+(?:\.\d+){0,1})%\s+(\d+,\d+)', re.IGNORECASE)
TAX_PERCEP_RE = re.compile(
    r'Iva Percepcion (\d+(?:\.\d+){0,1})%\s+(\d+,\d+)', re.IGNORECASE)
BILL_TOTAL_NEW_RE = re.compile(
    r'Total Factura Cta. 2/\d+\s*\$\s*((?:\d+\.){0,1}\d+,\d+)', re.IGNORECASE)
BILL_TOTAL_OLD_RE = re.compile(
    r'TOTAL FACTURA\s*\(IVA incluido\)\$\s*(\d+,\d+)', re.IGNORECASE)


class CellularDataParseError(Exception):
    """The phone data could not be parsed."""


class CellularConverter(PDFPageAggregator):
    """CellularConverter."""

    front_pages = ()
    table_pages = ()
    taxes_pages = ()
    taxes_fields = ()

    bill_number_length = 13
    bill_total_length = bill_debt_length = 8
    date_length = 10
    notes_length = 30
    plan_length = 6
    phone_length = 11

    def __init__(self, input_fd, *args, **kwargs):
        self._bill_date = None
        self._bill_number = None
        self._bill_total = None
        self._bill_debt = None
        self._bill_taxes = defaultdict(int)
        self._phone_data = []

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(input_fd)
        # Create a PDF document object that stores the document structure.
        self.doc = PDFDocument()
        # Connect the parser and document objects.
        parser.set_document(self.doc)
        self.doc.set_parser(parser)
        # Supply the password for initialization.
        # (If no password is set, give an empty string.)
        password = ''
        self.doc.initialize(password)
        # Check if the document allows text extraction. If not, abort.
        if not self.doc.is_extractable:
            raise PDFTextExtractionNotAllowed(
                'PDF text extraction not allowed.')
        # Create a PDF resource manager object that stores shared resources.
        self.rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = None  # LAParams()
        super(CellularConverter, self).__init__(self.rsrcmgr,
                                                laparams=laparams,
                                                *args, **kwargs)

    def is_phone_row(self, row):
        result = (len(row) == self.phone_length and PHONE_TOKEN in row and
                  row.strip().replace(PHONE_TOKEN, '').isdigit())
        return result

    def _process_phone_row(self, row):
        i = self.phone_length
        j = self.phone_length + self.notes_length
        phone = row[:i].replace(PHONE_TOKEN, '') if PHONE_TOKEN in row else ''
        if phone.isdigit():
            phone = int(phone)
            notes = row[i:j].strip()
            plan = row[j:j + self.plan_length].strip()
            rest = row[j + self.plan_length:]
            rest = PHONE_ROW_RE.findall(rest)
            self._phone_data.append(
                [phone, notes, plan] +
                [Decimal(i.strip().replace(',', '.')) for i in rest]
            )

    def _extract_all_text(self, page):
        lines = []
        for item in page:
            if getattr(item, 'get_text', None) is not None:
                t = item.get_text()
                lines.append(t)

        return ''.join(lines)

    def _extract_text(self, page, fn):
        last_text = []
        for item in page:
            if getattr(item, 'get_text', None) is not None:
                last_text.append(item.get_text())
            else:
                line = ''.join(last_text)
                last_text = []
                if line:
                    fn(line)

    def _process_bill_token(self, line, token, token_length):
        idx = line.find(token)
        data = None
        if idx != -1:
            idx += len(token)
            data = line[idx:idx + token_length]
        return data

    def _process_front_page(self, line):
        bill_date_str = self._process_bill_token(
            line, self.format['date_token'], self.date_length
        )
        if bill_date_str and not self._bill_date:
            self._bill_date = datetime.strptime(bill_date_str, "%d/%m/%Y")

        bill_number = self._process_bill_token(
            line, self.format['bill_number_token'],
            self.bill_number_length,
        )
        if bill_number and not self._bill_number:
            self._bill_number = bill_number

        bill_total = self._process_bill_token(
            line, self.format['bill_total_token'],
            self.bill_total_length,
        )
        if bill_total and not self._bill_total:
            self._bill_total = Decimal(
                bill_total.replace('.', '').replace(',', '.'))

        bill_debt = self._process_bill_token(
            line, self.format['bill_debt_token'],
            self.bill_debt_length,
        )
        if bill_debt and not self._bill_debt:
            self._bill_debt = Decimal(
                bill_debt.replace('.', '').replace(',', '.'))

    def process_front_page(self, layout):
        self._extract_text(layout, self._process_front_page)

    def process_phone_data(self, layout):
        if self._phone_data:
            return
        self._extract_text(layout, self._process_phone_row)

    def process_taxes(self, layout):
        all_text = self._extract_all_text(layout)
        results = []
        for regex in self.taxes_list:
            match = regex.search(all_text)
            if not match:
                continue
            results.extend(match.groups())

        groups = zip(self.taxes_fields, results)
        for k, v in groups:
            if ',' in v:
                v = v.replace('.', '').replace(',', '.')
            value = Decimal(v)
            if k.endswith('_tax'):
                value /= 100
            self._bill_taxes[k] = value

    def gather_phone_info(self):
        interpreter = PDFPageInterpreter(self.rsrcmgr, self)
        for page in self.doc.get_pages():
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = self.get_result()
            if layout.pageid in self.front_pages:
                self.process_front_page(layout)
            if layout.pageid in self.table_pages:
                self.process_phone_data(layout)
            if not self._bill_taxes:
                self.process_taxes(layout)

        if not self._phone_data:
            raise CellularDataParseError(
                'Could not parse file, got empty phone data (front_pages are '
                '%r, table_pages are %r)' %
                (self.front_pages, self.table_pages))

        self._bill_taxes['other_tax'] += self._bill_taxes.pop('percep_tax', 0)
        self._bill_taxes['other_tax_price'] += self._bill_taxes.pop(
            'percep_tax_price', 0)

        result = {
            'bill_date': self._bill_date, 'bill_number': self._bill_number,
            'bill_total': self._bill_total, 'bill_debt': self._bill_debt,
            'phone_data': self._phone_data,
        }
        result.update(self._bill_taxes)
        return result


class OldCellularConverter(CellularConverter):
    """CellularConverter."""

    format = dict(
        bill_debt_token='TOTAL A PAGAR$',
        bill_number_token='Factura Nro.',
        bill_total_token='TOTAL A PAGAR$',
        date_token='Fecha de Factura',
        join_token='',
    )
    front_pages = (1,)
    table_pages = (2, 7, 10)
    taxes_pages = (5, 6, 7, 8)
    taxes_fields = ('internal_tax', 'internal_tax_price',
                    'other_tax', 'other_tax_price', 'bill_total')
    taxes_list = (TAX_INTERNAL_RE, TAX_FINANC_RE, BILL_TOTAL_OLD_RE)


class NewCellularConverter(CellularConverter):
    """CellularConverter."""

    format = dict(
        bill_debt_token='TOTAL A PAGAR: $',
        bill_number_token='Factura Nro.: ',
        bill_total_token='TOTAL FACTURA: $',
        date_token='Fecha de Factura: ',
        join_token=' ',
    )
    front_pages = (2, 3, 4)
    table_pages = (3, 4, 5)
    taxes_pages = (3, 4)
    taxes_fields = ('internal_tax', 'internal_tax_price',
                    'percep_tax', 'percep_tax_price',
                    'other_tax', 'other_tax_price', 'bill_total')
    taxes_list = (TAX_INTERNAL_RE, TAX_PERCEP_RE, TAX_FINANC_RE,
                  BILL_TOTAL_NEW_RE)


def parse_file(fname, format='new'):
    try:
        input_fd = open(fname, 'rb')
    except IOError:
        return None

    try:
        if format == 'old':
            device = OldCellularConverter(input_fd)
        else:
            device = NewCellularConverter(input_fd)
        result = device.gather_phone_info()
    except PDFSyntaxError:
        result = {}

    return result


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    phone_data = data.pop('phone_data')
    print('-----------------------------')
    for k, v in data.iteritems():
        print(k, v)
    print('-----------------------------')
    print('\n'.join(map(lambda l: '|'.join(map(unicode, l)), phone_data)))
    print('-----------------------------')
