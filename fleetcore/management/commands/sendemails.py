# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import csv
import os

from collections import defaultdict
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from django.contrib.auth.models import User

from fleetcore.models import Plan, Phone


PEOPLE = {
    'Anthony': ['antoniolenton@gmail.com'],
    'Nelson': ['nelson.bordese@gmail.com'],
    'Natalia': ['mbordese@gmail.com', 'nataliabidart@gmail.com'],
    'Kuka': ['karimoroni@gmail.com'],
    'Walter': ['walteralini@gmail.com'],
}

ME = 'fleetthis@gmail.com'

PHONE_LINE = '%(real_user)s - Plan %(plan_name)s - %(number)s'

SUBJECT = 'Total del celu (consumo de %s)'

BODY = """Hola %(leader)s!

A continuación el detalle del consumo del mes %(month)s, detallado por nro. de
teléfono/persona:

%(phone_details)s
Total: $%(grand_total)s

Podrías por favor mandarme a este email el comprobante de pago
escaneado/fotografiado antes del 10 de este mes?

Muchas gracias!

Ah, y si podés mandarme un ack de que recibiste este mail, mejor.

Naty.

PD: este es un mail generado automáticamente, pero podés escribirme mail a
esta dirección que yo lo recibo sin drama (el mail cambió a uno dedicado a
esto de la flota, fijate que ahora es fleetthis@gmail.com).

PD2: este es el *último* mes en el que hay que usar la cuenta 613912138 para
pagar. A partir del mes que viene, habrá que usar otra cuenta, te paso los
datos cuando mande el consumo.

Detalles de los planes (con la info concreta de los mensajes):

%(plan_details)s
"""


def send_email_to_leader(who, month, phone_details, grand_total, plan_details):
    body = BODY % dict(leader=who, month=month, phone_details=phone_details,
                       grand_total=grand_total, plan_details=plan_details)
    subject = SUBJECT % month
    to_list = PEOPLE[who]
    to_list.append(ME)

    if os.getenv('DEBUG', True):
        print subject
        print body
    else:
        send_mail(subject, body, ME, to_list, fail_silently=False)


def helper(filename=None):
    today = datetime.today()
    last_month = today + timedelta(days=-28)
    totals = defaultdict(dict)

    if filename is None:
        filename = '%s/celu-%s-%02i.csv' % \
                   (last_month.year, last_month.year, last_month.month)
        print 'Looking for filename %s, is that correct?' % filename
        raw_input()

    assert os.path.exists(filename)

    reader = csv.reader(file(filename))
    for row in reader:
        if row[0] in PEOPLE and not row[1].startswith('$') and len(row) == 32:
            innerwho = PHONE_LINE % dict(real_user=row[1].decode('utf-8'),
                                         plan_name=row[4],
                                         number=row[2])
            totals[row[0]][innerwho] = float(row[-1].strip('$'))
        ##else:
        ##    print row

    all_plans = Plan.objects.all()
    month = last_month.strftime('%B %Y')
    for who, data in totals.iteritems():
        total = 0
        details = []
        for innerwho, amount in sorted(data.iteritems()):
            details.append('%s: $%s' % (innerwho, amount))
            total += amount

        phone_details = '\n'.join(details)
        plans = [p.description for p in all_plans if p.name in phone_details]

        send_email_to_leader(who=who, month=month, grand_total=total,
                             phone_details=phone_details,
                             plan_details='\n'.join(plans))


class Command(BaseCommand):
    help = 'Send emails with consumption summary to leaders.'

    def handle(self, *args, **options):
        if args:
            fname = args[0]
            assert os.path.exists(fname)
            helper(fname)
            return

        raise NotImplementedError()

        month = 'foo'
        ##this_bill = Bill.objects.get(id=bill_id)
        for user in User.objects.filter(is_staff=True):
            phones = Phone.objects.filter(user=user)
            if phones.count() == 0:
                continue

            details = []
            plans = set()
            for p in phones:
                details.append(PHONE_LINE % dict(real_user=p.notes,
                                                 plan_name=p.plan.name,
                                                 number=p.number) + ': $500')
                plans.add(p.plan.description)

            total = '100'
            ##Consumption.objects.filter(bill=this_bill).aggregate(
            ##  Sum('total'))['total__sum']
            send_email_to_leader(who=user.first_name, month=month,
                                 grand_total=total,
                                 phone_details='\n'.join(details),
                                 plan_details='\n'.join(plans))

        self.stdout.write('Successfully send all emails.\n')
