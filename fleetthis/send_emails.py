#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import smtplib

from collections import defaultdict
from datetime import datetime, timedelta
from email.charset import Charset
from email.mime.text import MIMEText

people = {
    'Anthony': ['antoniolenton@gmail.com'],
    'Douwe': ['douwe.judith@googlemail.com'],
    'Nelson': ['nelson.bordese@gmail.com'],
    'Nati': ['mbordese@gmail.com', 'nataliabidart@gmail.com'],
    'Kuka': ['karimoroni@gmail.com'],
    'Waldo': ['walteralini@gmail.com']}

today = datetime.today()
last_month = today + timedelta(days=-28)
totals = defaultdict(dict)
filename = '%s/celu-%s-%02i.csv' % \
           (last_month.year, last_month.year, last_month.month)
print 'Looking for filename %s, is that correct?' % filename
raw_input()

reader = csv.reader(file(filename))
for row in reader:
    if row[0] in people and not row[1].startswith('$') and len(row) == 32:
        innerwho = '%s - Plan %s - %s' % (row[2], row[4], row[1])
        totals[row[0]][innerwho] = float(row[-1].strip('$'))
    else:
        print row

PLANS = dict(TCM07="""DETALLE PLAN DE PRECIO: PLAN TCM07 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.22 $ 0.22
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $ 0.22 $ 0.22
Los SMS hacen clearing con el resto de las líneas en el mismo plan,
y cada línea aporta 100 SMS a la bolsa. Los SMS dentro de la bolsa de mensajes
salen $ 0.07, y por afuera cada uno sale $ 0.10

""",
             TCL16="""DETALLE PLAN DE PRECIO: PLAN TCL16 - Abono: $ 35.00 Pesos
Libres en el Plan:$ 35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24

""",
             TSC16="""DETALLE PLAN DE PRECIO: PLAN TSC16 - Abono: $ 35.00 Pesos
Libres en el Plan: $35.00
Precios sin imp ni cargo ENARD Ley 26573
Min. destino a teléfonos fijos: $ 0.27 $ 0.27
Min. destino a móviles del cliente: $ 0.00 $ 0.00
Min. destino a móviles: $0.27 $ 0.27
Los SMS no están incluídos en el abono, cada uno sale $ 0.24

""",
)

SUBJECT = 'Total del celu (consumo de %s)'
BODY = """Hola %s!

A continuación el detalle del consumo del mes %s, detallado por nro. de
teléfono/persona:

%s
Total: $%s

Podrías por favor mandarme a este email el comprobante de pago
escaneado/fotografiado antes del 10 de este mes?

Muchas gracias!

Ah, y si podés mandarme un ack de que recibiste este mail, mejor.

Naty.

PD: este es un mail generado automáticamente, pero podés escribirme mail a
esta dirección que yo lo recibo sin drama (el mail cambió a uno dedicado a
esto de la flota, fijate que ahora es fleetthis@gmail.com).

PD2: Este mes se consumieron todos los mensajes y todos los minutos! Aguante el
día del amigo (?).

Detalles de los planes (con la info concreta de los mensajes):

%s
"""

me = 'fleetthis@gmail.com'
month = last_month.strftime('%B %Y')
for who, data in totals.iteritems():
    total = 0
    detail = ''
    for innerwho, amount in sorted(data.iteritems()):
        detail += '%s: $%s\n' % (innerwho, amount)
        total += amount

    plans = ''
    for plan_code, plan_desc in PLANS.iteritems():
        if plan_code in detail:
            plans += plan_desc

    body = BODY % (who, month, detail, total, plans)
    msg = MIMEText(body) #, _charset='utf-8')
    msg['Subject'] = SUBJECT % month
    msg['From'] = me
    to_list = people[who]
    to_list.append(me)
    msg['To'] = ', '.join(to_list)

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
        server.login(me, 'aiKee!P0he')
        server.sendmail(me, to_list, msg.as_string())
        server.quit()
