# coding: utf-8

from django.core.management.base import BaseCommand

from fleetcore.models import Bill
from fleetcore.sendbills import BillSummarySender


class Command(BaseCommand):
    help = 'Send emails with consumption summary to leaders.'

    def handle(self, *args, **options):
        bill_id = int(args[0])
        this_bill = Bill.objects.get(id=bill_id)
        sender = BillSummarySender(bill=this_bill)
        sender.send_reports(dry_run=False)

        self.stdout.write('Successfully send all emails.\n')
