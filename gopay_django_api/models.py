from .signals import payment_changed
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
import copy
import gopay
import json


def payments():
    config = {
        'goid': str(settings.GOPAY_GOID),
        'clientId': str(settings.GOPAY_CLIENT_ID),
        'clientSecret': settings.GOPAY_CLIENT_SECRET,
        'isProductionMode': True if not hasattr(settings, 'GOPAY_IS_PRODUCTION') else settings.GOPAY_IS_PRODUCTION,
    }
    return gopay.payments(config)


class PaymentManager(models.Manager):

    def refresh_status(self, payment, force=False):
        response = payments().get_status(payment.gopay_id)
        if response.status_code != 200:
            raise Exception('There is an error during retrieving status of payment {}: {}.'.format(payment.gopay_id, response.json))
        status_before = copy.deepcopy(payment.status)
        if force or payment.is_status_different(response.json):
            payment.status = response.json
            payment.state = response.json['state']
            payment.refresh_counter += 1
            payment.save()
            payment_changed.send(sender=Payment, instance=payment, previous_status=status_before)
        return payment

    def create_contact(self, email, first_name=None, last_name=None, phone_number=None):
        """
        Create a contant which is later passed to payment.
        """
        result = {'email': email}
        if first_name is not None:
            result['first_name'] = first_name
        if last_name is not None:
            result['last_name'] = last_name
        if phone_number is not None:
            result['phone_number'] = phone_number
        return result

    def create_single_payment(self, contact, order_number, order_description, order_items, amount, return_url, currency=None, lang=None, additional_params=None):
        """
        Create a single payment.

        Args:
            contact: JSON describing a payer (see PaymentManager#create_contact)
            order_number: your identifier to the order which the payment is for
            order_description: desription of the order which is show to the
                user
            order_items: items in order which are shown to the other
                (item name -> amount)
            amount: total amount of money which will be paid
            returl_url: url for rediraction after payment is processed
            currency: default is set in settings (GOPAY_CURRENCY)
            lang: default is set in settings (GOPAY_LANG)
        Returns:
            dict: payment status
        """
        return self.create_payment(contact, {
            'amount': amount,
            'currency': currency if currency is not None else settings.GOPAY_CURRENCY,
            'lang': lang if lang is not None else settings.GOPAY_LANG,
            'additional_params': [] if additional_params is None else [{'name': key, 'value': str(value)} for key, value in additional_params.items()],
            'order_number': str(order_number),
            'order_description': order_description,
            'items': [{'name': key, 'amount': value} for key, value in order_items.items()],
            'callback': {
                'return_url': return_url,
                'notification_url': '{}{}'.format(settings.GOPAY_DOMAIN, reverse('gopay_notify')),
            },
        })

    def create_payment(self, contact, command):
        command = copy.deepcopy(command)
        command['payer'] = {
            'contact': contact,
            'default_payment_instrument': settings.GOPAY_DEFAULT_PAYMENT_INSTRUMENT,
            'allowed_payment_instruments': settings.GOPAY_ALLOWED_PAYMENT_INSTRUMENTS,
        }
        return self._create_payment(command)

    def _create_payment(self, command):
        response = payments().create_payment(command)
        if response.status_code != 200:
            raise Exception('There is an error during creating payment: {}.'.format(response.json))
        return self.create(
            gopay_id=response.json['id'],
            command=command,
            status=response.json,
            state=response.json['state']
        )


class Payment(models.Model):

    gopay_id = models.BigIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    refresh_counter = models.IntegerField(default=0)
    state = models.CharField(max_length=32, blank=True, null=True)
    _status = models.TextField()
    _command = models.TextField()

    def is_status_different(self, status):
        status_str = json.dumps(status, sort_keys=True)
        return self._status != status_str

    def _set_command(self, value):
        self._command = json.dumps(dict(value))

    def _get_command(self):
        return json.loads(self._command)

    def _set_status(self, value):
        self._status = json.dumps(value, sort_keys=True)

    def _get_status(self):
        return json.loads(self._status)

    command = property(_get_command, _set_command)
    status = property(_get_status, _set_status)

    objects = PaymentManager()
