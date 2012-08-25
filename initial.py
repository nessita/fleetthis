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

users = {}
for fn, ln, email in (
        ('Anthony', 'Lenton', 'antoniolenton@gmail.com'),
        ('Kuka', 'Moroni', 'karimoroni@gmail.com'),
        ('Matias', 'Bordese', 'mbordese@gmail.com'),
        ('Nelson', 'Bordese', 'nelsonbordese@gmail.com'),
        ('Natalia', 'Bidart', 'nataliabidart@gmail.com'),
        ('Walter', 'Alini', 'walteralini@gmail.com')):
    username = ('%s%s' % (fn[0], ln)).lower()
    users[username] = User.objects.create(
        username=username, email=email, first_name=fn, last_name=ln
        password=User.objects.make_random_password(),
    )


phones = (
    (1166936420, anthony, 'Vale'),
    (2314447229, anthony, 'ma de Vale'),
    (2314512571, anthony, 'Fede Berdion'),
    (2314516976, anthony, 'Miguel Berdion'),
    (3512255432, User.objects.get(first_name='Natalia'), 'Kuka Moroni'),
    (3512362650, User.objects.get(first_name='Matias'), 'himself'),
    (3513456948, User.objects.get(first_name='Laura'), 'herself'),
    (3513500734, anthony, 'himself'),
    (3513901750, User.objects.get(first_name='Walter'), 'himself'),
    (3513901899, User.objects.get(first_name='Natalia'), 'herself'),
)


tcl16 = plan['TCL16']
for n, u, m, p in phones:
    Phone.objects.create(number=n, user=u, notes=m, plan=tcl16)
