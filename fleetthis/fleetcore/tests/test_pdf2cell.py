import logging
import os

from datetime import datetime
from unittest import TestCase

from fleetthis.fleetcore import pdf2cell


THE_RESULT = {
    'bill_date': datetime(2012, 07, 26),
    'bill_number': '0588-50542628',
    'phone_data': [
        [1166936420, 'L, J', 'TSC16', 35.0, 45.0, 0.0, 103.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 45.0, 10.80, 0.0, 0.0, 90.80],
        [2314447229, 'L, J', 'TCM07', 35.0, 0.0, 0.0, 190.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 19.0, 0.0, 0.0, 0.0, 35.0],
        [2314512571, 'BERDION, FEDERICO MIGUEL', 'TCM07', 35.0, 0.0, 0.0,
         99.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 18.0, 0.10, 0.0, 0.0, 35.10],
        [2314516976, 'BERDION, MIGUEL ANGEL', 'TCM07', 35.0, 0.0, 0.0,
         108.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 35.0],
        [2914298833, 'TAPPA, RAYENT RAY', 'TCM07', 35.0, 0.0, 0.0,
         150.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 53.0, 3.80, 0.0, 0.0, 38.80],
        [3512255432, 'MORONI, KARINA', 'TCM07', 35.0, 0.0, 0.0,
         34.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 263.0, 3.40, 0.0, 0.0, 38.40],
        [3512362650, 'CTI8019', 'TCM07', 35.0, 0.0, 0.0, 34.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 27.0, 0.40, 0.0, 0.0, 35.40],
        [3513290201, 'LENTO, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         139.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 155.0, 5.85, 0.0, 0.0, 40.85],
        [3513290204, 'LENTO, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         17.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 137.0, 0.70, 0.0, 0.0, 35.70],
        [3513290207, 'LENTO, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         121.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 292.0, 7.50, 0.0, 0.0, 42.50],
        [3513456948, 'L, J', 'TCM07', 35.0, 0.0, 0.0, 100.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 126.0, 0.70, 0.0, 0.0, 35.70],
        [3513500734, 'LENTON, JUAN', 'TCM07', 35.0, 0.0, 0.0, 66.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 35.0],
        [3513901750, 'LENTON, JUAN', 'TCL16', 35.0, 60.0, 0.0,
         105.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 68.0, 0.0, 0.0, 0.0, 95.0],
        [3513901899, 'BIDART, NATALIA', 'TCM07', 35.0, 0.0, 0.0,
         27.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 29.0, 0.0, 0.0, 0.0, 35.0],
        [3516624678, 'PALANDRI, MIRTA IRENE', 'TCM07', 35.0, 0.0, 0.0,
         155.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 325.0, 2.50, 0.0, 0.0, 37.50],
        [3516624706, 'TAPP0A, TIKAEYEN', 'TCM07', 35.0, 0.0, 0.0,
         1115.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 440.0, 7.40, 0.0, 0.0, 42.40],
        [3516656710, 'LENTON, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         51.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 150.0, 3.10, 0.0, 0.0, 38.10],
        [3516656711, 'LENTON, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         18.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 0.0, 0.0, 0.0, 35.0],
        [3516656713, 'LENTON, JUAN ROLANDO', 'TCM07', 35.0, 0.0, 0.0,
         19.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 11.0, 0.10, 0.0, 0.0, 35.10],
        [3516847977, 'ARNOLETTI, MIRTHA ANA', 'TCM07', 35.0, 0.0, 0.0,
         45.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 28.0, 0.10, 0.0, 0.0, 35.10],
        [3516847979, 'DIAZZ, ANDREA PAOLA', 'TCM07', 35.0, 0.0, 0.0,
         37.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 302.0, 5.20, 0.0, 0.0, 40.20],
        [3875346390, 'LENTON, JUAN ROLANDO', 'TCM07', 0.0, 0.0, 0.0,
         43.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.66, 11.0, 0.0, 0.0, 0.0, 0.66],
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
