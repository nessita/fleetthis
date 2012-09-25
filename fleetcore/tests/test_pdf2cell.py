# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from fleetthis.fleetcore import pdf2cell


THE_RESULT = {
    'bill_date': datetime(2012, 07, 26),
    'bill_number': '0588-50542628',
    'phone_data': [
        [1166936420, 'L, J', 'TSC16', Decimal('35.0'), Decimal('45.0'),
         Decimal('0.0'), Decimal('103.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('45.0'), Decimal('10.80'), Decimal('0.0'), Decimal('0.0'),
         Decimal('90.80')],
        [2314447229, 'L, J', 'TCM07', Decimal('35.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('190.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('19.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('35.0')],
        [2314512571, 'BERDION, FEDERICO MIGUEL', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('99.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('18.0'),
         Decimal('0.10'), Decimal('0.0'), Decimal('0.0'), Decimal('35.10')],
        [2314516976, 'BERDION, MIGUEL ANGEL', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('108.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('35.0')],
        [2914298833, 'TAPPA, RAYENT RAY', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('150.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('53.0'),
         Decimal('3.80'), Decimal('0.0'), Decimal('0.0'), Decimal('38.80')],
        [3512255432, 'MORONI, KARINA', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('34.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('263.0'),
         Decimal('3.40'), Decimal('0.0'), Decimal('0.0'), Decimal('38.40')],
        [3512362650, 'CTI8019', 'TCM07', Decimal('35.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('34.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('27.0'), Decimal('0.40'),
         Decimal('0.0'), Decimal('0.0'), Decimal('35.40')],
        [3513290201, 'LENTO, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('139.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('155.0'),
         Decimal('5.85'), Decimal('0.0'), Decimal('0.0'), Decimal('40.85')],
        [3513290204, 'LENTO, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('17.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('137.0'),
         Decimal('0.70'), Decimal('0.0'), Decimal('0.0'), Decimal('35.70')],
        [3513290207, 'LENTO, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('121.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('292.0'),
         Decimal('7.50'), Decimal('0.0'), Decimal('0.0'), Decimal('42.50')],
        [3513456948, 'L, J', 'TCM07', Decimal('35.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('100.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('126.0'), Decimal('0.70'),
         Decimal('0.0'), Decimal('0.0'), Decimal('35.70')],
        [3513500734, 'LENTON, JUAN', 'TCM07', Decimal('35.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('66.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('35.0')],
        [3513901750, 'LENTON, JUAN', 'TCL16', Decimal('35.0'), Decimal('60.0'),
         Decimal('0.0'),
         Decimal('105.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('68.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('95.0')],
        [3513901899, 'BIDART, NATALIA', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('27.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('29.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('35.0')],
        [3516624678, 'PALANDRI, MIRTA IRENE', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('155.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('325.0'),
         Decimal('2.50'), Decimal('0.0'), Decimal('0.0'), Decimal('37.50')],
        [3516624706, 'TAPP0A, TIKAEYEN', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('1115.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('440.0'),
         Decimal('7.40'), Decimal('0.0'), Decimal('0.0'), Decimal('42.40')],
        [3516656710, 'LENTON, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('51.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('150.0'),
         Decimal('3.10'), Decimal('0.0'), Decimal('0.0'), Decimal('38.10')],
        [3516656711, 'LENTON, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('18.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('7.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('35.0')],
        [3516656713, 'LENTON, JUAN ROLANDO', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('19.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('11.0'),
         Decimal('0.10'), Decimal('0.0'), Decimal('0.0'), Decimal('35.10')],
        [3516847977, 'ARNOLETTI, MIRTHA ANA', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('45.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('28.0'),
         Decimal('0.10'), Decimal('0.0'), Decimal('0.0'), Decimal('35.10')],
        [3516847979, 'DIAZZ, ANDREA PAOLA', 'TCM07', Decimal('35.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('37.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('302.0'),
         Decimal('5.20'), Decimal('0.0'), Decimal('0.0'), Decimal('40.20')],
        [3875346390, 'LENTON, JUAN ROLANDO', 'TCM07', Decimal('0.0'),
         Decimal('0.0'), Decimal('0.0'),
         Decimal('43.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0'),
         Decimal('0.0'), Decimal('2.0'), Decimal('0.66'), Decimal('11.0'),
         Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.66')],
    ],
}


class ParsePDFTestCase(TestCase):
    """The test suite for the parse_pdf method."""

    fname = 'foo.pdf'

    def setUp(self):
        super(ParsePDFTestCase, self).setUp()
        self.addCleanup(lambda f: os.path.exists(f) and os.remove(f),
                        self.fname)
        self._enable_debug()

    def _enable_debug(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        self.addCleanup(logger.removeHandler, handler)

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
        fname = os.path.join(os.path.dirname(__file__), 'files', 'test.pdf')
        result = pdf2cell.parse_file(fname)
        self.assertEqual(result, THE_RESULT)
