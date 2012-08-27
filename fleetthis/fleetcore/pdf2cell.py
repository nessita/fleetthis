#!/usr/bin/env python

import logging
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


class CellularConverter(TextConverter):
    """CellularConverter."""

    start_x, start_y = 0, 0  # 222.5, 22.85
    processing_started = False
    table_page = 7

    def __init__(self, *args, **kwargs):
        super(CellularConverter, self).__init__(*args, **kwargs)
        self._data = []

    def process_item(self, item):
        if not isinstance(item, LTText):
            return

        origin_x = float(item.origin[X])
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
            self.last_x, self.last_y = item.origin

            if self.is_table_row:
                # store previous content
                self._data.append(map(str.strip, self.last_content))
            else:
                logging.debug("is not table row: %r", self.last_content)

            self.is_table_row = (PHONE_TOKEN in t and
                                 t.strip().replace(PHONE_TOKEN, '').isdigit())
            self.last_content = [t]  # new content
        elif item.origin[Y] == self.last_y:  # is the same table cell?
            self.last_content[-1] += t
        else:  # new table cell for current row
            assert self.last_x == origin_x
            self.last_y = item.origin[Y]
            self.last_content.append(t)

    def end_page(self, page):
        super(CellularConverter, self).end_page(page)

        self.last_x, self.last_y = self.start_x, self.start_y
        self.last_content = []
        self.is_table_row = False

        page = self.cur_item
        if page.id != self.table_page:
            # skip all pages that are not the cell phone listing
            return

        for child in page.objs:
            try:
                self.process_item(child)
            except AttributeError:
                pass

        self.to_file()

    def to_file(self):
        for row in self._data:
            self.outfp.write(FIELD_TOKEN.join(row) + '\n')


def parse_file(fname):
    rsrc = PDFResourceManager()
    device = CellularConverter(rsrc, sys.stdout)
    process_pdf(rsrc, device, fname)
    return device._data


if __name__ == '__main__':
    fname = sys.argv[1]  # fail if no filename is given
    data = parse_file(fname)
    print '-----------------------------'
    print data
    print '-----------------------------'
