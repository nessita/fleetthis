from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'fleetthis.settings'

from django.contrib.auth.models import User
from fleetthis.fleetcore.models import Plan, Phone


## (('XMD01', 2200, True), ('INTRC', 9507, False),
##  ('TCL16', 2900, False), ('', 0, False))
plans = {}
for i, j, k in (('TCL16', Decimal('27.00'), True),):
    plan[i] = Plan.objects.create(name=i, price=j, with_clearing=k)


User.objects.create_superuser(
    username='admin', email='fleetthis@gmail.com', password='123456')

leaders = (
    ('Anthony', 'Lenton', 'antoniolenton@gmail.com'),
    ('Kuka', 'Moroni', 'karimoroni@gmail.com'),
    ('Matias', 'Bordese', 'mbordese@gmail.com'),
    ('Nelson', 'Bordese', 'nelsonbordese@gmail.com'),
    ('Natalia', 'Bidart', 'nataliabidart@gmail.com'),
    ('Walter', 'Alini', 'walteralini@gmail.com')
)
users = {}
for fn, ln, email in leaders:
    username = ('%s%s' % (fn[0], ln)).lower()
    users[username] = User.objects.create(
        username=username, email=email, first_name=fn, last_name=ln,
        password=User.objects.make_random_password(),
    )


phones = (
    ('Anthony', 'Vale', 1166936420),
    ('Anthony', 'ma de Vale', 2314447229),
    ('Anthony', 'Fede Berdión', 2314512571),
    ('Anthony', 'Miguel Berdión', 2314516976),
    ('Anthony', 'Cuñada Vale', 2914298833),
    ('Kuka', 'Kuka', 3512255432),
    ('Nati', 'Mati', 3512362650),
    ('Waldo', 'Adrián Alini', 3513290201),
    ('Waldo', 'Aldo Alini', 3513290204),
    ('Waldo', 'Marianela Terragni', 3513290207),
    ('Mati', 'Lucía', 3513456948),
    ('Anthony', 'Anthony', 3513500734),
    ('Waldo', 'Waldo', 3513901750),
    ('Nati', 'Naty', 3513901899),
    ('Waldo', 'Adriana Spiazzi', 3516624678),
    ('Waldo', 'Franco Alini', 3516624706),
    ('Mati', 'Sofía', 3516656710),
    ('Mati', 'Nelson', 3516656711),
    ('Kuka', 'Damián', 3516656713),
    ('Waldo', 'Mirta Arnoletti', 3516847977),
    ('Waldo', 'Andrea Spiazzi', 3516847979),
)


tcl16 = plan['TCL16']
for leader, notes, number in phones:
    u = Leader.objects.get(first_name=leader)
    Phone.objects.create(number=number, user=u, notes=notes, plan=tcl16)
