from optparse import make_option
from django.core.management.base import BaseCommand
from gopay_django_api.models import Payment
from pprint import pprint


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--email',
            dest='email'
        ),
        make_option(
            '--order-number',
            dest='order_number'
        ),
        make_option(
            '--order-description',
            dest='order_description',
            default='No description'
        ),
        make_option(
            '--amount',
            dest='amount',
            type=float
        ),
        make_option(
            '--return_url',
            dest='return_url'
        ),
        make_option(
            '--order-item',
            dest='order_items',
            action='append',
            default=[]
        )
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
        pprint(payment.status)
