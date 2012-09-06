#!/usr/bin/env python

import logging
import os
import sys

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

    table_page = 7
    phone_length = 11
    notes_length = 30

    def __init__(self, input_fd, *args, **kwargs):
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

    def process_phone_row(self, row):
        i = self.phone_length
        j = self.phone_length + self.notes_length
        phone = row[:i]
        if self.is_phone_row(phone):
            notes = row[i:j].strip()
            rest = row[j:].split()
            plan = rest[0]
            rest = rest[1:]  # all the numeric values, isolate them for casting
            self._data.append(
                [phone, notes, plan] +
                [float(i.strip().replace(',', '.')) for i in rest]
            )

    def process_page(self, layout):
        last_text = []
        for item in layout:
            if getattr(item, 'get_text', None) is not None:
                last_text.append(item.get_text())
            else:
                line = ''.join(last_text)
                last_text = []
                if line:
                    self.process_phone_row(line)

    def gather_phone_info(self):
        interpreter = PDFPageInterpreter(self.rsrcmgr, self)
        for page in self.doc.get_pages():
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = self.get_result()
            if layout.pageid == 7:
                self.process_page(layout)
        return self._data


def parse_file(fname):
    try:
        input_fd = open(fname, 'rb')
    except IOError:
        return None

    try:
        device = CellularConverter(input_fd)
        result = device.gather_phone_info()
    except PDFSyntaxError:
        result = []

    return result


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    print '-----------------------------'
    print data
    print '-----------------------------'
