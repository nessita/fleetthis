# coding: utf-8

from datetime import datetime
from decimal import Decimal


PDF_PARSE_RESULT_1 = {
    'bill_date': datetime(2012, 9, 26),
    'bill_debt': Decimal('1871.22'),
    'bill_number': '0588-01407943',
    'bill_total': Decimal('1871.22'),
    'internal_tax': Decimal('0.0417'),
    'internal_tax_price': Decimal('55.38'),
    'other_tax': Decimal('0.04'),
    'other_tax_price': Decimal('51.96'),
    'phone_data': [
        ['1166936420', 'L, J', 'TCL16',
         Decimal('35.00'), Decimal('45.00'), Decimal('0.00'),
         Decimal('79.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('30.00'), Decimal('7.20'),
         Decimal('0.00'), Decimal('0.00'), Decimal('87.20')],
        ['2314447229', 'L, J', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('218.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('19.00'), Decimal('4.56'),
         Decimal('0.00'), Decimal('0.00'), Decimal('39.56')],
        ['2314512571', 'BERDION, FEDERICO MIGUEL', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('148.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('42.00'), Decimal('10.08'),
         Decimal('0.00'), Decimal('0.00'), Decimal('45.08')],
        ['2314516976', 'BERDION, MIGUEL ANGEL', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('85.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('35.00')],
        ['2914298833', 'TAPPA, RAYENT RAY', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('233.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('4.00'),
         Decimal('1.68'), Decimal('75.00'), Decimal('27.62'),
         Decimal('0.00'), Decimal('0.00'), Decimal('64.30')],
        ['3512255432', 'MORONI, KARINA', 'TCL16',
         Decimal('35.00'), Decimal('18.71'), Decimal('0.00'),
         Decimal('49.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('120.00'), Decimal('7.90'),
         Decimal('0.00'), Decimal('0.00'), Decimal('61.61')],
        ['3512362650', 'CTI8019', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('6.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('2.00'), Decimal('0.48'),
         Decimal('0.00'), Decimal('0.00'), Decimal('35.48')],
        ['3513290201', 'LENTO, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('31.81'), Decimal('0.00'),
         Decimal('141.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('168.00'), Decimal('9.71'),
         Decimal('0.00'), Decimal('0.00'), Decimal('76.52')],
        ['3513290204', 'LENTO, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('18.71'), Decimal('0.00'),
         Decimal('24.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('78.00'), Decimal('0.96'),
         Decimal('0.00'), Decimal('0.00'), Decimal('54.67')],
        ['3513290207', 'LENTO, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('31.81'), Decimal('0.00'),
         Decimal('129.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('370.00'), Decimal('46.99'),
         Decimal('0.00'), Decimal('0.00'), Decimal('113.80')],
        ['3513456948', 'L, J', 'TCL16',
         Decimal('35.00'), Decimal('18.71'), Decimal('0.00'),
         Decimal('47.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('66.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('53.71')],
        ['3513500734', 'LENTON, JUAN', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('31.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('4.00'),
         Decimal('1.02'), Decimal('5.00'), Decimal('1.20'),
         Decimal('0.00'), Decimal('57.04'), Decimal('94.26')],
        ['3513901750', 'LENTON, JUAN', 'TCL16',
         Decimal('35.00'), Decimal('60.00'), Decimal('0.00'),
         Decimal('125.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('86.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('95.00')],
        ['3513901899', 'BIDART, NATALIA', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('43.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('2.00'), Decimal('0.48'),
         Decimal('0.00'), Decimal('0.00'), Decimal('35.48')],
        ['3516624678', 'PALANDRI, MIRTA IRENE', 'TCL16',
         Decimal('35.00'), Decimal('31.81'), Decimal('0.00'),
         Decimal('106.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('295.00'), Decimal('28.99'),
         Decimal('0.00'), Decimal('0.00'), Decimal('95.80')],
        ['3516624706', 'TAPP0A, TIKAEYEN', 'TCL16',
         Decimal('35.00'), Decimal('41.16'), Decimal('0.00'),
         Decimal('894.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('439.00'), Decimal('44.85'),
         Decimal('0.00'), Decimal('0.00'), Decimal('121.01')],
        ['3516656710', 'LENTON, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('18.71'), Decimal('0.00'),
         Decimal('64.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('133.00'), Decimal('11.02'),
         Decimal('0.00'), Decimal('0.00'), Decimal('64.73')],
        ['3516656711', 'LENTON, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('22.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('7.00'), Decimal('1.68'),
         Decimal('0.00'), Decimal('0.00'), Decimal('36.68')],
        ['3516656713', 'LENTON, JUAN ROLANDO', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('19.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('12.00'), Decimal('2.88'),
         Decimal('0.00'), Decimal('0.00'), Decimal('37.88')],
        ['3516847977', 'ARNOLETTI, MIRTHA ANA', 'TCL16',
         Decimal('35.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('110.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('29.00'), Decimal('6.96'),
         Decimal('0.00'), Decimal('0.00'), Decimal('41.96')],
        ['3516847979', 'DIAZZ, ANDREA PAOLA', 'TCL16',
         Decimal('35.00'), Decimal('31.81'), Decimal('0.00'),
         Decimal('102.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('309.00'), Decimal('32.35'),
         Decimal('0.00'), Decimal('0.00'), Decimal('99.16')],
    ],
}

PDF_PARSE_RESULT_2 = {
    'bill_date': datetime(2017, 2, 26),
    'bill_debt': Decimal('2537.45'),
    'bill_number': '0960-00248687',
    'bill_total': Decimal('2285.58'),
    'internal_tax': Decimal('0.0417'),
    'internal_tax_price': Decimal('35.71'),
    'other_tax': Decimal('0.01'),
    'other_tax_price': Decimal('18.02'),
    'phone_data': [
        ['1166936420', 'L, J', 'TCL76', Decimal('90.00'),
         Decimal('60.00'), Decimal('45.00'), Decimal('30.31'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('1.00'), Decimal('0.00'), Decimal('0.00'), Decimal('105.00')],
        ['2314447229', 'L, J', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'),
         Decimal('41.67'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('23.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('45.00')],
        ['2314512571', 'BERDION, FEDERICO MIGUEL', 'TCL76',
         Decimal('90.00'), Decimal('0.00'),
         Decimal('45.00'), Decimal('10.06'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('8.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['2314516976', 'BERDION, MIGUEL ANGEL', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('31.09'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('3.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['2914298833', 'TAPPA, RAYENT RAY', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3447401068', '', 'TCL76', Decimal('90.00'),
         Decimal('60.00'), Decimal('45.00'), Decimal('22.49'),
         Decimal('1.00'), Decimal('0.50'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('1.00'), Decimal('0.00'), Decimal('0.00'), Decimal('105.50')],
        ['3447401133', '', 'TCL76', Decimal('90.00'),
         Decimal('60.00'), Decimal('45.00'), Decimal('137.26'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('16.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('105.00')],
        ['3447410644', '', 'TCL76', Decimal('90.00'),
         Decimal('0.00'), Decimal('45.00'), Decimal('488.48'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('5.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3512255432', 'MORONI, KARINA', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('62.04'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('87.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3512362650', 'CTI8019', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3513290201', 'LENTO, JUAN ROLANDO', 'TCL76', Decimal('90.00'),
         Decimal('130.00'), Decimal('45.00'), Decimal('110.61'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('38.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('175.00')],
        ['3513290207', 'LENTO, JUAN ROLANDO', 'TCL76',
         Decimal('90.00'), Decimal('60.00'), Decimal('45.00'),
         Decimal('61.09'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('12.00'), Decimal('0.00'), Decimal('240.00'),
         Decimal('345.00')],
        ['3513456948', 'L, J', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('78.45'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('34.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3513901750', 'LENTON, JUAN', 'TCL76', Decimal('90.00'),
         Decimal('60.00'), Decimal('45.00'), Decimal('256.58'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('7.00'), Decimal('0.00'), Decimal('0.00'), Decimal('105.00')],
        ['3516624706', 'EZIO ALINI, FRANCO', 'TCL76', Decimal('90.00'),
         Decimal('215.00'), Decimal('45.00'), Decimal('269.38'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('3.00'), Decimal('0.00'), Decimal('0.00'), Decimal('260.00')],
        ['3516656710', 'LENTON, JUAN ROLANDO', 'TCL76', Decimal('90.00'),
         Decimal('60.00'), Decimal('45.00'), Decimal('131.30'),
         Decimal('3.00'), Decimal('1.50'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('5.00'), Decimal('0.00'), Decimal('0.00'), Decimal('106.50')],
        ['3516656711', 'LENTON, JUAN ROLANDO', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('67.14'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('9.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3516656713', 'LENTON, JUAN ROLANDO', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('1.21'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('8.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')],
        ['3516667637', '', 'TCL76',
         Decimal('90.00'), Decimal('0.00'), Decimal('45.00'), Decimal('44.49'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'),
         Decimal('42.00'), Decimal('0.00'), Decimal('0.00'), Decimal('45.00')]
    ],
}
