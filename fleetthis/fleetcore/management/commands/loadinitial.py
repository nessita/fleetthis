from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User
from fleetthis.fleetcore.models import Fleet, Plan, Phone


PLANS = (
    # ('XMD01', 2200, True), ('INTRC', 9507, False),
    ('TCM07', Decimal('35.00'), True, 130, Decimal('0.22'), 100, Decimal('0.07'),
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
    ('TSC16', Decimal('35.00'), True, 130, Decimal('0.27'), 0, Decimal('0.24'),
     """DETALLE PLAN DE PRECIO: PLAN TSC16 - Abono: $ 35.00 Pesos
Libres en el Plan: $35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24.
"""),
    ('TCL16', Decimal('35.00'), True, 130, Decimal('0.27'), 0, Decimal('0.24'),
     """DETALLE PLAN DE PRECIO: PLAN TCL16 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24.
"""),
)

LEADERS = (
    ('Anthony', 'Lenton', 'antoniolenton@gmail.com'),
    ('Kuka', 'Moroni', 'karimoroni@gmail.com'),
    ('Matias', 'Bordese', 'mbordese@gmail.com'),
    ('Nelson', 'Bordese', 'nelsonbordese@gmail.com'),
    ('Natalia', 'Bidart', 'nataliabidart@gmail.com'),
    ('Walter', 'Alini', 'walteralini@gmail.com')
)

PHONES = (
    ('Anthony', 'Vale', 1166936420),
    ('Anthony', 'ma de Vale', 2314447229),
    ('Anthony', 'Fede Berdión', 2314512571),
    ('Anthony', 'Miguel Berdión', 2314516976),
    ('Anthony', 'Cuñada Vale', 2914298833),
    ('Kuka', 'Kuka', 3512255432),
    ('Natalia', 'Mati', 3512362650),
    ('Walter', 'Adrián Alini', 3513290201),
    ('Walter', 'Aldo Alini', 3513290204),
    ('Walter', 'Marianela Terragni', 3513290207),
    ('Nelson', 'Lucía', 3513456948),
    ('Anthony', 'Anthony', 3513500734),
    ('Walter', 'Walter', 3513901750),
    ('Natalia', 'Naty', 3513901899),
    ('Walter', 'Adriana Spiazzi', 3516624678),
    ('Walter', 'Franco Alini', 3516624706),
    ('Nelson', 'Sofía', 3516656710),
    ('Nelson', 'Nelson', 3516656711),
    ('Kuka', 'Damián', 3516656713),
    ('Walter', 'Mirta Arnoletti', 3516847977),
    ('Walter', 'Andrea Spiazzi', 3516847979),
)


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() > 0:
            raise CommandError('Can not be run twice.')

        User.objects.create_superuser(
            username='admin', email='fleetthis@gmail.com', password='admin')

        users = {}
        for fn, ln, email in LEADERS:
            username = ('%s%s' % (fn[0], ln)).lower()
            users[username] = User.objects.create(
                username=username, email=email, first_name=fn, last_name=ln,
                password=User.objects.make_random_password(), is_staff=True,
            )

        the_fleet = Fleet.objects.create(
            owner=users['walini'], account_number=725615496,
            email='fleetthis@gmail.com', provider='Claro',
        )
        naty = users['nbidart']
        for username, user in users.iteritems():
            profile = user.get_profile()
            profile.leader = naty
            profile.fleet = the_fleet
            profile.save()

        plans = {}
        for i, j, k, mins, min_price, sms, sms_price, desc in PLANS:
            plans[i] = Plan.objects.create(name=i, price=j, with_clearing=k,
                                           included_minutes=mins,
                                           min_price=min_price,
                                           included_sms=sms, sms_price=sms_price,
                                           description=desc)

        tcl16 = plans['TCL16']
        for leader, notes, number in PHONES:
            u = User.objects.get(first_name=leader)
            Phone.objects.create(number=number, user=u, notes=notes, plan=tcl16)

        self.stdout.write('Successfully loaded initial data.\n')
