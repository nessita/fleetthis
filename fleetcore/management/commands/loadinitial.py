# coding: utf-8

import os
import unicodedata

from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from fleetcore.models import DataPack, Fleet, Plan, Phone, SMSPack


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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
    # same line, it changed number, *3* times
    (3516624678, 200), (1133471500, 200), (3447448141, 200),
    (3516847979, 200),
    (3516624706, 300),
))

USERS = {
    ('Anthony', 'Lenton', 'antoniolenton@gmail.com'): [
        ('Valeria', 'Berdión', 'berdion@gmail.com'),
        ('ma de Vale', 'Berdión', 'antoniolenton+madevale@gmail.com'),
        ('Federico', 'Berdión', 'antoniolenton+federico@gmail.com'),
        ('Miguel', 'Berdión', 'antoniolenton+miguel@gmail.com'),
        ('Familia', 'Berdión', 'antoniolenton+misc@gmail.com'),
    ],

    ('Karina', 'Moroni', 'karimoroni@gmail.com'): [
        ('Damián', 'Barsotti', 'damian.barsotti@gmail.com'),
    ],

    ('Natalia', 'Bidart', 'nataliabidart@gmail.com'): [
        ('Matías', 'Bordese', 'mbordese@gmail.com'),
        ('Marcos', 'Dione', 'mr.styxman@gmail.com'),
    ],

    ('Nelson', 'Bordese', 'nelsonbordese@gmail.com'): [
        ('Lucía', 'Bordese', 'lubordese@gmail.com'),
        ('Sofía', 'Bordese', 'sofiabordese@gmail.com'),
    ],

    ('Walter', 'Alini', 'walteralini@gmail.com'): [
        ('Adrián', 'Alini', 'alini.adrian@gmail.com'),
        ('Aldo', 'Alini', 'aldoalini@gmail.com'),
        ('Marianela', 'Terragni', 'marianelaterragni@hotmail.com'),
        ('Adriana', 'Spiazzi', 'adrianaspiazzi@yahoo.com.ar'),
        ('Franco', 'Alini', 'francoalini@gmail.com'),
        ('Mirta', 'Arnoletti', 'aldoalini+mirta@gmail.com'),
        ('Andrea', 'Spiazzi', 'andreapspiazzi@hotmail.com'),
    ],
    ('Douwe', '1', 'douwe.judith+390@googlemail.com'): [
        ('Douwe', '2', 'douwe.judith+564@googlemail.com'),
    ],
}

PHONES = [
    (3513500734, 'antoniolenton@gmail.com', '2007-02-17 12:56:07', None),
    (1166936420, 'berdion@gmail.com', '2007-03-02 13:33:46', None),
    (2314447229, 'antoniolenton+madevale@gmail.com',
     '2007-03-02 13:23:35', None),
    (2314512571, 'antoniolenton+federico@gmail.com',
     '2005-01-17 21:28:43', None),
    (2314516976, 'antoniolenton+miguel@gmail.com',
     '2005-10-13 11:23:28', None),
    (2914298833, 'antoniolenton+misc@gmail.com',
     '2007-01-08 19:14:33', None),
    (3512255432, 'karimoroni@gmail.com', '2007-12-03 10:23:09', None),
    (3516656713, 'damian.barsotti@gmail.com', '2009-11-26 10:22:41', None),
    (3513901899, 'nataliabidart@gmail.com', '2007-08-21 17:18:05', None),
    (3512362650, 'mbordese@gmail.com', '2008-05-14 10:20:52', None),
    (3516625555, 'mr.styxman@gmail.com', '2007-02-17 00:00:00',
     '2011-06-29 00:00:00'),
    (3516656711, 'nelsonbordese@gmail.com', '2009-11-26 10:22:38', None),
    (3513456948, 'lubordese@gmail.com', '2007-01-12 17:22:12', None),
    (3516656710, 'sofiabordese@gmail.com', '2009-11-26 10:22:31', None),
    (3513901750, 'walteralini@gmail.com', '2007-08-21 15:54:46', None),
    (3513290201, 'alini.adrian@gmail.com', '2009-07-02 11:36:42', None),
    (3513290204, 'aldoalini@gmail.com', '2009-07-02 11:36:50', None),
    (3513290207, 'marianelaterragni@hotmail.com', '2009-07-02 11:36:52', None),
    (3516624678, 'adrianaspiazzi@yahoo.com.ar',
     '2007-03-27 09:51:50', '2012-10-25 19:13:00'),
    (1133471500, 'adrianaspiazzi@yahoo.com.ar',
     '2012-10-25 19:13:37', '2013-02-06 18:35:00'),
    (3447448141, 'adrianaspiazzi@yahoo.com.ar', '2013-02-06 18:35:15', None),
    (3516624706, 'francoalini@gmail.com', '2007-12-03 10:22:45', None),
    (3516847977, 'aldoalini+mirta@gmail.com', '2009-12-02 14:11:01', None),
    (3516847979, 'andreapspiazzi@hotmail.com',
     '2009-12-02 14:11:12', None),
    (3875346390, 'douwe.judith+390@googlemail.com',
     '2007-02-17 00:00:00', '2012-07-19 00:00:00'),
    (3875342564, 'douwe.judith+564@googlemail.com',
     '2007-02-17 00:00:00', '2012-07-19 00:00:00'),
]

FLEETS = (
    (231842055, 'johnlenton@gmail.com'),
    (613912138, 'nataliabidart@gmail.com'),
    (725615496, 'fleetthis@gmail.com'),
)


def normalize(word):
    res = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
    return res.lower().replace(' ', '')


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
        for (i, j, mins, price_min, sms, price_sms, min_clearing, sms_clearing,
             desc) in PLANS:
            plans[i] = Plan.objects.create(
                name=i, price=j, included_min=mins, price_min=price_min,
                included_sms=sms, price_sms=price_sms, description=desc,
                with_min_clearing=min_clearing, with_sms_clearing=sms_clearing,
            )

        def create_user(fn, ln, email, leader=None):
            username = normalize(fn) + normalize(ln)
            user = User.objects.create(
                username=username, email=email, first_name=fn, last_name=ln,
                password=User.objects.make_random_password(),
                is_staff=leader is None,
            )
            profile = user.get_profile()
            profile.leader = admin if leader is None else leader
            profile.save()
            return user

        for values, children in USERS.items():
            leader = create_user(*values)
            for values in children:
                create_user(*values, leader=leader)

        tcl16 = plans['TCL16']

        def create_phone(number, email, active_since, active_to):
            user = User.objects.get(email=email)

            active_since = datetime.strptime(active_since, DATETIME_FORMAT)
            if active_to is not None:
                active_to = datetime.strptime(active_to, DATETIME_FORMAT)
            p = Phone.objects.create(
                number=number, user=user, notes='', current_plan=tcl16,
                active_since=active_since, active_to=active_to,
            )

            if number in DATA_PACKS_BINDING:
                price = DATA_PACKS_BINDING[number]
                p.data_pack = DataPack.objects.get(price=price)

            if number in SMS_PACKS_BINDINGS:
                units = SMS_PACKS_BINDINGS[number]
                p.sms_pack = SMSPack.objects.get(units=units)

            p.save()

        for values in PHONES:
            create_phone(*values)

        for account, email in FLEETS:
            fleet = Fleet.objects.create(
                user=admin, account_number=account,
                email=email, provider='Claro',
            )
            if account == 725615496:
                fleet.report_consumption_template = REPORT_TEMPLATE
                fleet.save()

        # update site configuration
        current_site = Site.objects.get_current()
        current_site.domain = settings.SITE_DOMAIN
        current_site.name = 'Fleet This'
        current_site.save()

        self.stdout.write('Successfully loaded initial data.\n')
