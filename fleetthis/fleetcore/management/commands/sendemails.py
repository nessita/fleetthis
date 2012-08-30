#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import smtplib

from collections import defaultdict
from datetime import datetime, timedelta
from email.charset import Charset
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from django.contrib.auth.models import User

from fleetthis.fleetcore.models import Plan, Phone


PEOPLE = {
    u'Anthony': [u'antoniolenton@gmail.com'],
    u'Nelson': [u'nelson.bordese@gmail.com'],
    u'Natalia': [u'mbordese@gmail.com', u'nataliabidart@gmail.com'],
    u'Kuka': [u'karimoroni@gmail.com'],
    u'Walter': [u'walteralini@gmail.com'],
}

ME = 'fleetthis@gmail.com'

PHONE_LINE = u'%(real_user)s - Plan %(plan_name)s - %(number)s'

SUBJECT = u'Total del celu (consumo de %s)'

BODY = u"""Hola %(leader)s!

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

Detalles de los planes (con la info concreta de los mensajes):

%(plan_details)s
"""


def send_email_to_leader(who, month, phone_details, grand_total, plan_details):
    body = BODY % dict(leader=who, month=month, phone_details=phone_details,
                       grand_total=grand_total, plan_details=plan_details)
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = SUBJECT % month
    msg['From'] = ME
    to_list = PEOPLE[who]
    to_list.append(ME)
    msg['To'] = ', '.join(to_list)

    print msg.as_string()
    return

    if os.getenv('DEBUG', True):
        print msg.as_string()
    else:
        # smtp.gmail.com (use authentication)
        # Use Authentication: Yes
        # Port for TLS/STARTTLS: 587
        # Port for SSL: 465
        server = smtplib.SMTP('smtp.gmail.com', port=587)
        #server.set_debuglevel(1)
        server.starttls()
        server.login(ME, 'aiKee!P0he')
        server.sendmail(ME, to_list, msg.as_string())
        server.quit()


def helper():
    today = datetime.today()
    last_month = today + timedelta(days=-28)
    totals = defaultdict(dict)
    filename = '%s/celu-%s-%02i.csv' % \
               (last_month.year, last_month.year, last_month.month)
    print 'Looking for filename %s, is that correct?' % filename
    raw_input()

    reader = csv.reader(file(filename))
    for row in reader:
        if row[0] in PEOPLE and not row[1].startswith('$') and len(row) == 32:
            innerwho = PHONE_LINE % dict(real_user=row[2], plan_name=row[4],
                                         number=row[1])
            totals[row[0]][innerwho] = float(row[-1].strip('$'))
        else:
            print row

    all_plans = Plans.objects.all()
    month = last_month.strftime('%B %Y')
    for who, data in totals.iteritems():
        total = 0
        details = []
        for innerwho, amount in sorted(data.iteritems()):
            detail.append('%s: $%s' % (innerwho, amount))
            total += amount
        plans = [p.description for p in all_plans if p.name in detail]

        send_email_to_leader(who=who, month=month, grand_total=total,
                             phone_details='\n'.join(detail),
                             plan_details='\n'.join(plans))


class Command(BaseCommand):
    help = 'Send emails with consumption summary to leaders.'

    def handle(self, *args, **options):
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
