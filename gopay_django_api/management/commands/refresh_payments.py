from optparse import make_option
from django.core.management.base import BaseCommand
from gopay_django_api.models import Payment
from clint.textui import progress


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--state',
            dest='state',
            default=None
        ),
        make_option(
            '--force',
            dest='force',
            action='store_true',
            default=False
        ),
    )

    def handle(self, *args, **options):
        for payment in progress.bar(Payment.objects.all()):
            if options['state'] is not None and payment.state != options['state']:
                continue
            Payment.objects.refresh_status(payment, force=options['force'])
