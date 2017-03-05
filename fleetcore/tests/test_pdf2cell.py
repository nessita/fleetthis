# coding: utf-8

import logging
import os

from io import BytesIO
from unittest import TestCase

from fleetcore import pdf2cell
from fleetcore.tests.results import PDF_PARSE_RESULT_1, PDF_PARSE_RESULT_2


class ParsePDFTestCase(TestCase):
    """The test suite for the parse_pdf method."""

    fname = 'foo.pdf'
    real_pdf = 'test_1.pdf'
    real_result = PDF_PARSE_RESULT_1
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

    def test_empty_file(self):
        result = self.parse(content=b'')
        self.assertEqual(result, {})

    def test_invalid_pdf_file(self):
        result = self.parse(content=b'30947hksl.nfa;kfjawlfhnqwlvlc.;vlasmlna')
        self.assertEqual(result, {})

    def test_real_pdf(self):
        fname = os.path.join(os.path.dirname(__file__), 'files', self.real_pdf)
        with open(fname, 'rb') as f:
            content = f.read()

        result = self.parse(content=content)

        self.assertEqual(sorted(result.keys()),
                         sorted(self.real_result.keys()))
        for k in result:  # ('bill_date', 'bill_number', 'phone_data'):
            self.assertEqual(result[k], self.real_result[k])

        self.assertEqual(result, self.real_result)


class ParseNoOtherTaxPDFTestCase(ParsePDFTestCase):
    """The test suite for the parse_pdf method."""

    real_pdf = 'test_2.pdf'
    real_result = PDF_PARSE_RESULT_2
