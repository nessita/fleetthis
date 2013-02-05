# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import os

from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User
from fleetcore.models import DataPack, Fleet, Plan, Phone, SMSPack


with open(os.path.join(os.path.dirname(__file__), 'report_template.txt')) as f:
    REPORT_TEMPLATE = f.read()


PLANS = (
    # ('XMD01', 2200, True), ('INTRC', 9507, False),
    ('', Decimal('0'), 0, Decimal('0'), 0, Decimal('0'), False, False,
     "DUMMY PLAN."),
    ('TCM07', Decimal('35.00'), 127,
     Decimal('0.22'), 100, Decimal('0.07'), True, True,
     """DETALLE PLAN DE PRECIO: PLAN TCM07 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.22 $ 0.22
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $ 0.22 $ 0.22
Los SMS hacen clearing con el resto de las líneas en el mismo plan,
y cada línea aporta 100 SMS a la bolsa. Los SMS dentro de la bolsa de mensajes
salen $ 0.07, y por afuera cada uno sale $ 0.10.
"""),
    ('TSC16', Decimal('35.00'), 129, Decimal('0.27'), 0, Decimal('0.24'),
     False, False,
     """DETALLE PLAN DE PRECIO: PLAN TSC16 - Abono: $ 35.00 Pesos
Libres en el Plan: $35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24.
"""),
    ('TCL16', Decimal('35.00'), 129, Decimal('0.27'), 0, Decimal('0.24'),
     True, False,
     """DETALLE PLAN DE PRECIO: PLAN TCL16 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24.
"""),
)

DATA_PACKS = (
    (None, Decimal('45.00')),
    (None, Decimal('50.00')),
)

SMS_PACKS = (
    (50, Decimal('6.00')),
    (100, Decimal('11.00')),
    (200, Decimal('19.00')),
    (300, Decimal('25.00')),
    (400, Decimal('30.00')),
    (500, Decimal('36.00')),
    (1000, Decimal('56.00')),
)

DATA_PACKS_BINDING = dict((
    (1166936420, 45),
    (3513901750, 50),
    (3516847979, 50),
))

SMS_PACKS_BINDINGS = dict((
    (3516656713, 50),
    (3516847977, 50),
    (3512255432, 100),
    (3513456948, 100),
    (3516656710, 100),
    (3513290204, 100),
    (3513901750, 100),
    (3513290201, 200),
    (3513290207, 200),
    (3516624678, 200), (1133471500, 200),  # same line, it changed number
    (3516847979, 200),
    (3516624706, 300),
))

PHONES = {
    (3513500734, 'Anthony', 'Lenton', 'antoniolenton@gmail.com'): [
        (1166936420, 'Valeria', 'Berdión', 'berdion@gmail.com'),
        (2314447229, 'ma de Vale', 'Berdión', ''),
        (2314512571, 'Federico', 'Berdión', ''),
        (2314516976, 'Miguel', 'Berdión', ''),
        (2914298833, 'Familia', 'Berdión', ''),
    ],

    (3512255432, 'Karina', 'Moroni', 'karimoroni@gmail.com'): [
        (3516656713, 'Damián', 'Barsotti', 'damian.barsotti@gmail.com'),
    ],

    (3513901899, 'Natalia', 'Bidart', 'nataliabidart@gmail.com'): [
        (3512362650, 'Matías', 'Bordese', 'mbordese@gmail.com'),
        (3516625555, 'Marcos', 'Dione', ''),
    ],

    (3516656711, 'Nelson', 'Bordese', 'nelsonbordese@gmail.com'): [
        (3513456948, 'Lucía', 'Bordese', 'lubordese@gmail.com'),
        (3516656710, 'Sofía', 'Bordese', 'sofiabordese@gmail.com'),
    ],

    (3513901750, 'Walter', 'Alini', 'walteralini@gmail.com'): [
        (3513290201, 'Adrián', 'Alini', 'alini.adrian@gmail.com'),
        (3513290204, 'Aldo', 'Alini', 'aldoalini@gmail.com'),
        (3513290207, 'Marianela', 'Terragni', 'marianelaterragni@hotmail.com'),
        (3516624678, 'Adriana', 'Spiazzi', 'adrianaspiazzi@yahoo.com.ar'),
        (1133471500, 'Adriana', 'Spiazzi', 'adrianaspiazzi@yahoo.com.ar'),
        (3516624706, 'Franco', 'Alini', 'francoalini@gmail.com'),
        (3516847977, 'Mirta', 'Arnoletti', 'aldoalini@gmail.com'),
        (3516847979, 'Andrea', 'Spiazzi', 'andreapspiazzi@hotmail.com'),
    ],
    (3875346390, 'Douwe', '', ''): [
        (3875342564, 'Douwe', '', ''),
    ],
}

FLEETS = (
    (231842055, 'johnlenton@gmail.com'),
    (613912138, 'nataliabidart@gmail.com'),
    (725615496, 'fleetthis@gmail.com'),
)


class Command(BaseCommand):

    help = 'Loading initial data.'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() > 0:
            raise CommandError('Can not be run twice.')

        admin_email = settings.ADMIN_EMAIL
        admin_pwd = settings.ADMIN_PASSWORD
        admin = User.objects.create_superuser(
            username='admin', email=admin_email, password=admin_pwd)

        for kbs, price in DATA_PACKS:
            DataPack.objects.create(kbs=kbs, price=price)

        for sms, price in SMS_PACKS:
            SMSPack.objects.create(units=sms, price=price)

        plans = {}
        for i, j, mins, price_min, sms, price_sms, desc in PLANS:
            plans[i] = Plan.objects.create(
                name=i, price=j, included_min=mins, price_min=price_min,
                included_sms=sms, price_sms=price_sms, description=desc,
                with_min_clearing=min_clering, with_sms_clearing=sms_clearing,
            )

        tcl16 = plans['TCL16']

        def create_phone(fn, ln, number, email, leader=None):
            user = User.objects.create(
                username=number, email=email, first_name=fn, last_name=ln,
                password=User.objects.make_random_password(),
                is_staff=leader is None,
            )
            profile = user.get_profile()
            profile.leader = admin if leader is None else leader
            profile.save()

            p = Phone.objects.create(number=number, user=user,
                                     notes='', plan=tcl16)

            if number in DATA_PACKS_BINDING:
                price = DATA_PACKS_BINDING[number]
                p.data_pack = DataPack.objects.get(price=price)

            if number in SMS_PACKS_BINDINGS:
                units = SMS_PACKS_BINDINGS[number]
                p.sms_pack = SMSPack.objects.get(units=units)

            p.save()

            return user

        for (n, first_name, last_name, email), phones in PHONES.iteritems():
            leader = create_phone(first_name, last_name, n, email)
            for n, fn, ln, e in phones:
                create_phone(fn, ln, n, email=e, leader=leader)

        for account, email in FLEETS:
            fleet = Fleet.objects.create(
                user=admin, account_number=account,
                email=email, provider='Claro',
            )
            if account == 725615496:
                fleet.report_consumption_template = REPORT_TEMPLATE
                fleet.save()

        self.stdout.write('Successfully loaded initial data.\n')
