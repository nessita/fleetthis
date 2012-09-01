#!/usr/bin/env python

import logging
import os
import sys

from pdfminer.converter import (
    enc,
    TextConverter,
    LTText,
)
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

FIELD_TOKEN = '|'
PHONE_TOKEN = '-'
X = 0
Y = 1


def is_phone_row(row):
    result = (len(row) == 11 and PHONE_TOKEN in row and
              row.strip().replace(PHONE_TOKEN, '').isdigit())
    return result


class CellularConverter(PDFPageAggregator):  # TextConverter):
    """CellularConverter."""

    start_x, start_y = 0, 0  # 222.5, 22.85
    processing_started = False
    table_page = 7

    def __init__(self, *args, **kwargs):
        super(CellularConverter, self).__init__(*args, **kwargs)
        self._data = []

    def process_item(self, item):
        print '\n\n\n======PROCESS PAGE==========', item
        if not isinstance(item, LTText):
            return

        origin_x = float(item.x0)
        if origin_x < self.start_x:
            return

        t = enc(item.text, self.codec)
        if is_phone_row(t):
            self.processing_started = True

        if not self.processing_started:
            return

        logging.debug('%r ===== %r %r %r %r %r', item.text, t, origin_x,
                      self.start_x, self.last_x, origin_x > self.last_x)

        if origin_x > self.last_x:  # is a new row?
            self.last_x, self.last_y = item.x0, item.y0

            if self.is_table_row:
                # store previous content
                self._data.append(map(str.strip, self.last_content))
            else:
                logging.debug("is not table row: %r", self.last_content)

            self.is_table_row = (PHONE_TOKEN in t and
                                 t.strip().replace(PHONE_TOKEN, '').isdigit())
            self.last_content = [t]  # new content
        elif item.y0 == self.last_y:  # is the same table cell?
            self.last_content[-1] += t
        else:  # new table cell for current row
            assert self.last_x == origin_x
            self.last_y = item.y0
            self.last_content.append(t)

    def begin_page(self, page, ctm=None):
        super(CellularConverter, self).begin_page(page, ctm)

    def end_page(self, page):
        super(CellularConverter, self).end_page(page)

        self.last_x, self.last_y = self.start_x, self.start_y
        self.last_content = []
        self.is_table_row = False

        logging.debug('ZARAZA: %r', page)
        if self.pageno != self.table_page + 1:
            # skip all pages that are not the cell phone listing
            return

        for child in self.cur_item._objs:
            try:
                self.process_item(child)
            except AttributeError:
                pass

        self.to_file()

    def to_file(self):
        for row in self._data:
            self.outfp.write(FIELD_TOKEN.join(row) + '\n')


def from_docs(fname):
    # Open a PDF file.
    fp = open(fname, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    doc = PDFDocument()
    # Connect the parser and document objects.
    parser.set_document(doc)
    doc.set_parser(parser)
    # Supply the password for initialization.
    # (If no password is set, give an empty string.)
    password = ''
    doc.initialize(password)
    # Check if the document allows text extraction. If not, abort.
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = CellularConverter(rsrcmgr, laparams=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #import pdb; pdb.set_trace()
    for page in doc.get_pages():
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        print '\n\n===LAYOUT FINISHED: ', layout, layout.pageid

    ##converter = PDFConverter(rsrcmgr, sys.stdout)


def parse_file(fname, debug=False):
    rsrcmgr = PDFResourceManager()
    if debug:
        fout = sys.stderr
    else:
        fout = open(os.devnull, 'w')

    try:
        fp = open(fname, 'rb')
    except IOError:
        return None

    try:
        device = CellularConverter(rsrcmgr, fout)
        process_pdf(rsrcmgr, device, fp)
        result = device._data
    except PDFSyntaxError:
        result = []

    return result


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    print '-----------------------------'
    print data
    print '-----------------------------'
