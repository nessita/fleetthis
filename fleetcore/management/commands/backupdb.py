# coding: utf-8

import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = 'Email the current sqlite DB as a backup measure.'

    def handle(self, *args, **options):
        # grab db path
        db_path = settings.DATABASES['default']['NAME']
        if not os.path.exists(db_path):
            raise CommandError('DB path %r does not exist.\n' % db_path)

        msg = EmailMessage(subject='FT DB backup', to=[settings.ADMIN_EMAIL])
        msg.attach_file(db_path, 'application/octet-stream')
        msg.send()
        self.stdout.write('Successfully sent email.\n')
