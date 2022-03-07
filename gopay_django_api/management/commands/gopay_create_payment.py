from optparse import make_option
from django.core.management.base import BaseCommand
from gopay_django_api.models import Payment
from pprint import pprint


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            dest='email',
        )
        parser.add_argument(
            '--order-number',
            dest='order_number',
        )
        parser.add_argument(
            '--order-description',
            dest='order_description',
            default='No description',
        )
        parser.add_argument(
            '--amount',
            dest='amount',
            type=float,
        )
        parser.add_argument(
            '--return_url',
            dest='return_url',
        )
        parser.add_argument(
            '--order-item',
            dest='order_items',
            action='append',
            default=[],
        )

    def handle(self, *args, **options):
        payment = Payment.objects.create_single_payment(
            Payment.objects.create_contact(options['email']),
            options['order_number'],
            options['order_description'],
            {item.split(':')[0]: float(item.split(':')[1]) for item in options['order_items']},
            options['amount'],
            options['return_url']
        )
        print(payment)
