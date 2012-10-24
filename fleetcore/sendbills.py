# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import csv
import os

from collections import defaultdict
from datetime import datetime, timedelta

from django.core.mail import send_mail
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

OJO: Este es el PRIMER mes en el que hay que usar la cuenta NUEVA (número
725615496) para pagar. A partir de ahora, te recomiendo romper las facturas
anteriores que usabas para pagar, para evitar confusiones.

En un ratito te mando otro mail con un pdf que podés imprimir, y que contiene
el código de barras "corto" que se puede usar para los pagos abiertos de
Claro.

Por otro lado, es importante notar que los totales de este mes incluyen, para
aquellas líneas que pidieron packs de mensajes, el proporcional del pack de
Septiembre más el abono adelantado del pack de Octubre (o sea, casi 2 packs
enteros).

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
    subject = SUBJECT % month
    to_list = PEOPLE[who]
    to_list.append(ME)

    if os.getenv('DEBUG', True):
        print('==============================================================')
        print(subject)
        print('--------------------------------------------------------------')
        print(body)
        print('==============================================================')
    else:
        send_mail(subject, body, ME, to_list, fail_silently=False)


class BillSummarySender(object):
    """Send emails with consumption summary to leaders."""

    def __init__(self, bill):
        self.bill = bill

    def send_emails(self, dry_run=True):
        for leader, data in self.bill.details.items:

            header = 'Consumptions for {leader} - Total ${total}'
            header = header.format(leader=leader.get_full_name(),
                                    total=data.total)
            details = []
            for c in data.consumptions:
                innerwho = PHONE_LINE % dict(
                    real_user=c.phone.user.get_full_name(),
                    plan_name=c.phone.plan.name,
                    number=c.phone.number,
                )
                details.append('%s: $%s' % (innerwho, c.total))

            plan_details = '\n'.join(
                self.bill.consumption_set.values(
                    'phone__plan', flat=True).distinct().values('description')
            )
            send_email_to_leader(who=leader.get_full_name(),
                                 month=self.bill.billing_date.month,
                                 grand_total=data.total,
                                 phone_details='\n'.join(details),
                                 plan_details='')
