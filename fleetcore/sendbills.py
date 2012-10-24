# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


SUBJECT = 'Total del celu (consumo de %s)'


class BillSummarySender(object):
    """Send emails with consumption summary to leaders."""

    def __init__(self, bill):
        self.bill = bill

    def send_reports(self, dry_run=True):
        for leader, data in self.bill.details.iteritems():
            body = render_to_string('report.txt',
                                    {'data': data, 'leader': leader})
            subject = SUBJECT % self.bill.billing_date.strftime('%B')
            to_list = [leader.email]
            to_list.append(settings.ADMIN_EMAIL)

            send_mail(subject, body, settings.ADMIN_EMAIL, to_list,
                      fail_silently=False)
