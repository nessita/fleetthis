# coding: utf-8

import logging
import json
import os

from decimal import Decimal
from io import BytesIO
from unittest import TestCase, SkipTest

from fleetcore import pdf2cell


class ParsePDFTestCase(TestCase):
    """The test suite for the parse_pdf method."""

    fname = 'foo.pdf'
    real_pdf = 'test_1.pdf'
    maxDiff = None

    def setUp(self):
        super(ParsePDFTestCase, self).setUp()
        self.addCleanup(lambda f: os.path.exists(f) and os.remove(f),
                        self.fname)
        logging.getLogger().setLevel(logging.ERROR)

    def parse(self, content, **kwargs):
        file_obj = BytesIO(content)
        result = pdf2cell.parse_file(file_obj, **kwargs)
        return result

    def process_real_file(self, pdffile, resultfile):
        fname = os.path.join(os.path.dirname(__file__), 'files', pdffile)
        if not os.path.exists(fname):
            raise SkipTest('Real file %r does not exist.' % fname)
        expected = os.path.join(os.path.dirname(__file__), 'files', resultfile)
        if not os.path.exists(expected):
            raise SkipTest('Parse result file %r does not exist.' % expected)

        with open(fname, 'rb') as f:
            content = f.read()

        with open(expected, 'r') as f:
            expected = json.loads(f.read())

        result = self.parse(content=content)

        self.assertCountEqual(result.keys(), expected.keys())

        self.assertEqual(
            result['bill_date'].isoformat(), expected['bill_date'])
        self.assertEqual(result['bill_debt'], Decimal(expected['bill_debt']))
        self.assertEqual(result['bill_number'], expected['bill_number'])
        self.assertEqual(result['bill_total'], Decimal(expected['bill_total']))
        self.assertEqual(
            result['internal_tax'], Decimal(expected['internal_tax']))
        self.assertEqual(
            result['internal_tax_price'],
            Decimal(expected['internal_tax_price']))
        self.assertEqual(result['other_tax'], Decimal(expected['other_tax']))
        self.assertEqual(
            result['other_tax_price'], Decimal(expected['other_tax_price']))
        expected_phone_data = []
        for row in expected['phone_data']:
            expected_phone_data.append(row[:3] + [Decimal(i) for i in row[3:]])
        self.assertEqual(result['phone_data'], expected_phone_data)

    def test_empty_file(self):
        result = self.parse(content=b'')
        self.assertEqual(result, {})

    def test_invalid_pdf_file(self):
        result = self.parse(content=b'30947hksl.nfa;kfjawlfhnqwlvlc.;vlasmlna')
        self.assertEqual(result, {})

    def test_real_pdf_1(self):
        self.process_real_file('test_1.pdf', 'test_1.json')

    def test_real_pdf_2(self):
        self.process_real_file('test_2.pdf', 'test_2.json')
