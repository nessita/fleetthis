import logging
import os

from unittest import TestCase

from fleetthis.fleetcore import pdf2cell


THE_RESULT = [
    ['11-66936420', 'L, J', 'TSC16', '35,00', '45,00', '0,00', '103,00',
     '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '45,00', '10,80',
     '0,00', '0,00', '90,80'],
    ['2314-447229', 'L, J', 'TCM07', '35,00', '0,00', '0,00', '190,00', '0,00',
     '0,00', '0,00', '0,00', '0,00', '0,00', '19,00', '0,00', '0,00', '0,00',
     '35,00'],
    ['2314-512571', 'BERDION, FEDERICO MIGUEL', 'TCM07', '35,00', '0,00',
     '0,00', '99,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '18,00',
     '0,10', '0,00', '0,00', '35,10'],
    ['2314-516976', 'BERDION, MIGUEL ANGEL', 'TCM07', '35,00', '0,00',
     '0,00', '108,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00',
     '0,00', '0,00', '0,00', '35,00'],
    ['291-4298833', 'TAPPA, RAYENT RAY', 'TCM07', '35,00', '0,00',
     '0,00', '150,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '53,00',
     '3,80', '0,00', '0,00', '38,80'],
    ['351-2255432', 'MORONI, KARINA', 'TCM07', '35,00', '0,00', '0,00',
     '34,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '263,00',
     '3,40', '0,00', '0,00', '38,40'],
    ['351-2362650', 'CTI8019', 'TCM07', '35,00', '0,00', '0,00', '34,00',
     '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '27,00', '0,40',
     '0,00', '0,00', '35,40'],
    ['351-3290201', 'LENTO, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '139,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '155,00',
     '5,85', '0,00', '0,00', '40,85'],
    ['351-3290204', 'LENTO, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '17,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '137,00',
     '0,70', '0,00', '0,00', '35,70'],
    ['351-3290207', 'LENTO, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '121,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '292,00',
     '7,50', '0,00', '0,00', '42,50'],
    ['351-3456948', 'L, J', 'TCM07', '35,00', '0,00', '0,00', '100,00',
     '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '126,00', '0,70', '0,00',
     '0,00', '35,70'],
    ['351-3500734', 'LENTON, JUAN', 'TCM07', '35,00', '0,00', '0,00', '66,00',
     '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00',
     '0,00', '35,00'],
    ['351-3901750', 'LENTON, JUAN', 'TCL16', '35,00', '60,00', '0,00',
     '105,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '68,00', '0,00',
     '0,00', '0,00', '95,00'],
    ['351-3901899', 'BIDART, NATALIA', 'TCM07', '35,00', '0,00', '0,00',
     '27,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '29,00', '0,00',
     '0,00', '0,00', '35,00'],
    ['351-6624678', 'PALANDRI, MIRTA IRENE', 'TCM07', '35,00', '0,00', '0,00',
     '155,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '325,00',
     '2,50', '0,00', '0,00', '37,50'],
    ['351-6624706', 'TAPP0A, TIKAEYEN', 'TCM07', '35,00', '0,00', '0,00',
     '1115,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '440,00',
     '7,40', '0,00', '0,00', '42,40'],
    ['351-6656710', 'LENTON, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '51,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '150,00', '3,10',
     '0,00', '0,00', '38,10'],
    ['351-6656711', 'LENTON, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '18,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '7,00', '0,00',
     '0,00', '0,00', '35,00'],
    ['351-6656713', 'LENTON, JUAN ROLANDO', 'TCM07', '35,00', '0,00', '0,00',
     '19,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '11,00', '0,10',
     '0,00', '0,00', '35,10'],
    ['351-6847977', 'ARNOLETTI, MIRTHA ANA', 'TCM07', '35,00', '0,00', '0,00',
     '45,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '28,00', '0,10',
     '0,00', '0,00', '35,10'],
    ['351-6847979', 'DIAZZ, ANDREA PAOLA', 'TCM07', '35,00', '0,00', '0,00',
     '37,00', '0,00', '0,00', '0,00', '0,00', '0,00', '0,00', '302,00', '5,20',
     '0,00', '0,00', '40,20'],
    ['387-5346390', 'LENTON, JUAN ROLANDO', 'TCM07', '0,00', '0,00', '0,00',
     '43,00', '0,00', '0,00', '0,00', '0,00', '2,00', '0,66', '11,00', '0,00',
     '0,00', '0,00', '0,66'],
]


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
        self.assertEqual(result, [])

    def test_invalid_pdf_file(self):
        with open(self.fname, 'w') as f:
            f.write('30947hknsl.nfa;kfjawlfhnqwlvlc.;vlasmlna')

        assert os.path.exists(self.fname)

        result = pdf2cell.parse_file(self.fname)
        self.assertEqual(result, [])

    def test_real_pdf(self):
        fname = os.path.join(os.path.dirname(__file__), 'files', 'test.pdf')
        #result = pdf2cell.parse_file(fname)
        result = pdf2cell.from_docs(fname)
        self.assertEqual(result, THE_RESULT)
