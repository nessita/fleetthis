from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'fleetthis.settings'

from decimal import Decimal

from django.contrib.auth.models import User
from fleetthis.fleetcore.models import Plan, Phone


all_plans = (
    # ('XMD01', 2200, True), ('INTRC', 9507, False),
    # ('TCL16', 2900, False), ('', 0, False))
    ('TCL16', Decimal('35.00'), True, 130, Decimal('0.27'), Decimal('0.1'),
     """DETALLE PLAN DE PRECIO: PLAN TCL16 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.10"""),
)
leaders = (
    ('Anthony', 'Lenton', 'antoniolenton@gmail.com'),
    ('Kuka', 'Moroni', 'karimoroni@gmail.com'),
    ('Matias', 'Bordese', 'mbordese@gmail.com'),
    ('Nelson', 'Bordese', 'nelsonbordese@gmail.com'),
    ('Natalia', 'Bidart', 'nataliabidart@gmail.com'),
    ('Walter', 'Alini', 'walteralini@gmail.com')
)
phones = (
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


def main():
    plans = {}
    for i, j, k, l, min_price, sms_price, desc in all_plans:
        plans[i] = Plan.objects.create(name=i, price=j, with_clearing=k,
                                       minutes=l, min_price=min_price,
                                       sms_price=sms_price, description=desc)

    User.objects.create_superuser(
        username='admin', email='fleetthis@gmail.com', password='admin')

    users = {}
    for fn, ln, email in leaders:
        username = ('%s%s' % (fn[0], ln)).lower()
        users[username] = User.objects.create(
            username=username, email=email, first_name=fn, last_name=ln,
            password=User.objects.make_random_password(),
        )

    tcl16 = plans['TCL16']
    for leader, notes, number in phones:
        u = User.objects.get(first_name=leader)
        Phone.objects.create(number=number, user=u, notes=notes, plan=tcl16)


if __name__ == '__main__':
    main()
