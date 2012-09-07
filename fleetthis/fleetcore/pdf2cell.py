#!/usr/bin/env python

import logging
import os
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


class CellularConverter(PDFPageAggregator):
    """CellularConverter."""

    bill_number_length = 13
    date_length = 10
    notes_length = 30
    phone_length = 11
    table_page = 7

    def __init__(self, input_fd, *args, **kwargs):
        self._bill_date = None
        self._bill_number = None
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
            rest = row[j:].split()
            plan = rest[0]
            rest = rest[1:]  # all the numeric values, isolate them for casting
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

    def _process_front_page(self, line):
        idx = line.find('Fecha de Factura')
        if idx != 1 and self._bill_date is None:
            idx += len('Fecha de Factura')
            bill_date_str = line[idx:idx + self.date_length]
            self._bill_date = datetime.strptime(bill_date_str, "%d/%m/%Y")

        idx = line.find('Factura Nro.')
        if idx != 1 and self._bill_number is None:
            idx += len('Factura Nro.')
            self._bill_number = line[idx:idx + self.bill_number_length]

    def gather_phone_info(self):
        interpreter = PDFPageInterpreter(self.rsrcmgr, self)
        for page in self.doc.get_pages():
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = self.get_result()
            if layout.pageid == 1:
                self._extract_text(layout, self._process_front_page)
            elif layout.pageid == self.table_page:
                self._extract_text(layout, self._process_phone_row)

        return {'bill_date': self._bill_date, 'bill_number': self._bill_number,
                'phone_data': self._data}


def parse_file(fname):
    try:
        input_fd = open(fname, 'rb')
    except IOError:
        return None

    try:
        device = CellularConverter(input_fd)
        result = device.gather_phone_info()
    except PDFSyntaxError:
        result = {}

    return result


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    print '-----------------------------'
    print data
    print '-----------------------------'
