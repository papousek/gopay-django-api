from clint.textui import progress
from django.core.management.base import BaseCommand
from django.db import transaction
from gopay_django_api.models import Payment
from optparse import make_option


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--state',
            dest='state',
            default=None,
        )
        parser.add_argument(
            '--force',
            dest='force',
            action='store_true',
            default=False,
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            for payment in progress.bar(Payment.objects.all()):
                if options['state'] is not None and payment.state != options['state']:
                    continue
                Payment.objects.refresh_status(payment, force=options['force'])
