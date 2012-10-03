# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User
from fleetcore.models import DataPack, Fleet, Plan, Phone, SMSPack


PLANS = (
    # ('XMD01', 2200, True), ('INTRC', 9507, False),
    ('TCM07', Decimal('35.00'), 130,
     Decimal('0.22'), 100, Decimal('0.07'),
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
    ('TSC16', Decimal('35.00'), 130, Decimal('0.27'), 0,
     Decimal('0.24'),
     """DETALLE PLAN DE PRECIO: PLAN TSC16 - Abono: $ 35.00 Pesos
Libres en el Plan: $35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24.
"""),
    ('TCL16', Decimal('35.00'), 130, Decimal('0.27'), 0, Decimal('0.24'),
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
    (50, Decimal('5.50')),
    (100, Decimal('10.00')),
    (200, Decimal('17.00')),
    (300, Decimal('22.00')),
    (400, Decimal('27.00')),
    (500, Decimal('32.50')),
    (1000, Decimal('49.90')),
)

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
    ],

    (3516656711, 'Nelson', 'Bordese', 'nelsonbordese@gmail.com'): [
        (3513456948, 'Lucía', 'Bordese', 'lubordese@gmail.com'),
        (3516656710, 'Sofía', 'Bordese', 'sofiabordese@gmail.com'),
    ],

    (3513901750, 'Walter', 'Alini', 'walteralini@gmail.com'): [
        (3513290201, 'Adrián', 'Alini', ''),
        (3513290204, 'Aldo', 'Alini', 'aldoalini@gmail.com'),
        (3513290207, 'Marianela', 'Terragni', 'marianelaterragni@hotmail.com'),
        (3516624678, 'Adriana', 'Spiazzi', 'adrianaspiazzi@yahoo.com.ar'),
        (3516624706, 'Franco', 'Alini', 'francoalini@gmail.com'),
        (3516847977, 'Mirta', 'Arnoletti', ''),
        (3516847979, 'Andrea', 'Spiazzi', ''),
    ],
    (3875346390, 'Douwe', '', 'douwe@example.com'): [
    ],
}


class Command(BaseCommand):

    help = 'Loading initial data.'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() > 0:
            raise CommandError('Can not be run twice.')

        admin_email = settings.ADMIN_EMAIL
        admin_pwd = settings.ADMIN_PASSWORD
        admin = User.objects.create_superuser(
            username='admin', email=admin_email, password=admin_pwd)

        the_fleet = Fleet.objects.create(
            user=admin, account_number=725615496,
            email='fleetthis@gmail.com', provider='Claro',
        )

        for kbs, price in DATA_PACKS:
            DataPack.objects.create(kbs=kbs, price=price)

        for sms, price in SMS_PACKS:
            SMSPack.objects.create(units=sms, price=price)

        plans = {}
        for i, j, mins, min_price, sms, sms_price, desc in PLANS:
            plans[i] = Plan.objects.create(
                name=i, price=j, included_min=mins, min_price=min_price,
                included_sms=sms, sms_price=sms_price, description=desc,
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

            Phone.objects.create(number=number, user=user,
                                 notes='', plan=tcl16)

            return user

        for (n, first_name, last_name, email), phones in PHONES.iteritems():
            leader = create_phone(first_name, last_name, n, email)
            for n, fn, ln, e in phones:
                create_phone(fn, ln, n, email=e, leader=leader)

        self.stdout.write('Successfully loaded initial data.\n')
