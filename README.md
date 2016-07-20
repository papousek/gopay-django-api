# GoPay Django API

Django app to integrate GoPay into your project.

Communication with GoPay API is fully handled by
[gopay-python-api](https://github.com/gopaycommunity/gopay-python-api). For
now, We have implemented just a part of the API:

* creating a single payment

Feel free to add other parts!

## Configuration

Add `gopay_django_api` into *installed_apps* and set these parameters:

```
GOPAY_DOMAIN = <your domain>
GOPAY_GOID = <goid>
GOPAY_CLIENT_ID = <client id>
GOPAY_CLIENT_SECRET = <client secret>
GOPAY_IS_PRODUCTION = <False if you want to use testing environment, True otherwise>
GOPAY_LANG = <language of the gateway, e.g., Language.CZECH>
GOPAY_DEFAULT_PAYMENT_INSTRUMENT = <default payment method, e.g., PaymentInstrument.PAYMENT_CARD>
GOPAY_ALLOWED_PAYMENT_INSTRUMENTS = <list of all available payment methods, e.g., [PaymentInstrument.PAYMENT_CARD>
GOPAY_CURRENCY = <currency, e.g., Currency.CZECH_CROWNS>
```

Add this somewhere into your urls:

```python
url(r'^gopay/', include('gopay_django_api.urls'))
```

## Usage

```python
from gopay_django_api.models import Payment
from gopay_django_api.signals import payment_changed


contact = Payment.objects.create_contact(email='customer@domain.com')
payment = Payment.objects.create_single_payment(
    cotact=contact,
    order_number=42,
    order_description='Description of the order.',
    order_items={'item_name': 100},
    amount=100,
    return_url='http://domain.com/something'
)


@receiver(payment_changed)
def check_payment(sender, instance, previous_state, **kwargs):
    # something
    pass
```

