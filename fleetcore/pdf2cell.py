# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os
import re
import sys

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
 INCLUDED_MIN, EXCEEDED_MIN, EXCEEDED_MIN_PRICE,
 NDL_MIN, NDL_PRICE, IDL_MIN, IDL_PRICE,
 SMS, SMS_PRICE, EQUIPMENT_PRICE, OTHER_PRICE, TOTAL_PRICE) = range(18)

PHONE_TOKEN = '-'

OLD_FORMAT = dict(
    bill_debt_token='TOTAL A PAGAR$',
    bill_number_token='Factura Nro.',
    bill_total_token='TOTAL A PAGAR$',
    date_token='Fecha de Factura',
    front_page=1,
    join_token='',
    table_page=7,
)

NEW_FORMAT = dict(
    bill_debt_token='TOTAL A PAGAR: $',
    bill_number_token='Factura Nro.: ',
    bill_total_token='TOTAL FACTURA: $',
    date_token='Fecha de Factura: ',
    front_page=2,
    join_token=' ',
    table_page=3,
)

PHONE_ROW_RE = re.compile(r'\s*(\d+,\d{2})\s*')


class CellularConverter(PDFPageAggregator):
    """CellularConverter."""

    formats = dict(new=NEW_FORMAT, old=OLD_FORMAT)
    bill_number_length = 13
    bill_total_length = bill_debt_length = 8
    date_length = 10
    notes_length = 30
    plan_length = 6
    phone_length = 11

    def __init__(self, input_fd, format, *args, **kwargs):
        self.bill_format = self.formats[format]
        self._bill_date = None
        self._bill_number = None
        self._bill_total = None
        self._bill_debt = None
        self._data = []
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
            raise PDFTextExtractionNotAllowed
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
            self._data.append(
                [phone, notes, plan] +
                [Decimal(i.strip().replace(',', '.')) for i in rest]
            )

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
            line, self.bill_format['date_token'], self.date_length
        )
        if bill_date_str and not self._bill_date:
            self._bill_date = datetime.strptime(bill_date_str, "%d/%m/%Y")

        bill_number = self._process_bill_token(
            line, self.bill_format['bill_number_token'],
            self.bill_number_length,
        )
        if bill_number and not self._bill_number:
            self._bill_number = bill_number

        bill_total = self._process_bill_token(
            line, self.bill_format['bill_total_token'],
            self.bill_total_length,
        )
        if bill_total and not self._bill_total:
            self._bill_total = Decimal(
                bill_total.replace('.', '').replace(',', '.'))

        bill_debt = self._process_bill_token(
            line, self.bill_format['bill_debt_token'],
            self.bill_debt_length,
        )
        if bill_debt and not self._bill_debt:
            self._bill_debt = Decimal(
                bill_debt.replace('.', '').replace(',', '.'))

    def gather_phone_info(self):
        interpreter = PDFPageInterpreter(self.rsrcmgr, self)
        for page in self.doc.get_pages():
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = self.get_result()
            if layout.pageid == self.bill_format['front_page']:
                self._extract_text(layout, self._process_front_page)
            elif layout.pageid == self.bill_format['table_page']:
                self._extract_text(layout, self._process_phone_row)

        result = {
            'bill_date': self._bill_date, 'bill_number': self._bill_number,
            'bill_total': self._bill_total, 'bill_debt': self._bill_debt,
            'phone_data': self._data,
        }
        return result


def parse_file(fname, format='new'):
    try:
        input_fd = open(fname, 'rb')
    except IOError:
        return None

    try:
        device = CellularConverter(input_fd, format=format)
        result = device.gather_phone_info()
    except PDFSyntaxError:
        result = {}

    return result


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    print('-----------------------------')
    print(data)
    print('-----------------------------')
