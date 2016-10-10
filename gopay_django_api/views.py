from .models import Payment
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


@transaction.atomic()
def notify(request):
    payment_id = request.GET['id']
    payment = get_object_or_404(Payment, gopay_id=payment_id)
    Payment.objects.refresh_status(payment)
    return HttpResponse('ok', status=200)
