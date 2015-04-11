# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import logging
import os

from unittest import TestCase

from fleetcore import pdf2cell
from fleetcore.tests.results import PDF_PARSE_RESULT, PDF_PARSE_NEW_RESULT


class ParsePDFTestCase(TestCase):
    """The test suite for the parse_pdf method."""

    fname = 'foo.pdf'
    format = 'old'
    real_pdf = 'test.pdf'
    real_result = PDF_PARSE_RESULT

    def setUp(self):
        super(ParsePDFTestCase, self).setUp()
        self.addCleanup(lambda f: os.path.exists(f) and os.remove(f),
                        self.fname)
        logging.getLogger().setLevel(logging.ERROR)

    def test_non_existing_file(self):
        assert not os.path.exists(self.fname)
        result = pdf2cell.parse_file(self.fname)
        self.assertEqual(result, None)

    def test_empty_file(self):
        with open(self.fname, 'w') as f:
            pass

        assert os.path.exists(self.fname)
        with open(self.fname) as f:
            assert f.read() == ''

        result = pdf2cell.parse_file(self.fname)
        self.assertEqual(result, {})

    def test_invalid_pdf_file(self):
        with open(self.fname, 'w') as f:
            f.write('30947hknsl.nfa;kfjawlfhnqwlvlc.;vlasmlna')

        assert os.path.exists(self.fname)

        result = pdf2cell.parse_file(self.fname)
        self.assertEqual(result, {})

    def test_real_pdf(self):
        fname = os.path.join(os.path.dirname(__file__), 'files', self.real_pdf)
        result = pdf2cell.parse_file(fname, format=self.format)

        self.assertEqual(sorted(result.keys()),
                         sorted(self.real_result.keys()))
        for k in result:  # ('bill_date', 'bill_number', 'phone_data'):
            self.assertEqual(result[k], self.real_result[k])

        self.assertEqual(result, self.real_result)


class ParseNewPDFTestCase(ParsePDFTestCase):
    """The test suite for the parse_pdf method using the new PDF format."""

    format = 'new'
    real_pdf = 'test_new.pdf'
    real_result = PDF_PARSE_NEW_RESULT
