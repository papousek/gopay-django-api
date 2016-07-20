from django.conf.urls import url
from . import views


urlpatterns = [
    url("^notify/$", views.notify, name="gopay_notify"),
]
