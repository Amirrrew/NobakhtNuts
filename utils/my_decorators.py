
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import requests
from django.db.models import Case, When, Value, IntegerField,Q
import os

from account_module.models import Notification, User, BlackList_phones


def permission_checker_decorator_factory(data = None):
    def permission_checker_decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse('admin_login'))
        return wrapper
    return permission_checker_decorator



def send_sms(phone):
    data = {'to': phone}
    response = requests.post(settings.SMS_API_KEY, json=data)
    print(response.json())
    return response.json()


def check_phone_blacklisted(phone):
    blacklisted = BlackList_phones.objects.filter(phone=phone).exists()
    if blacklisted:
        return True
    else: return False


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        return False
    else:
        return True


def filter_products(request, queryset):

    queryset = queryset.annotate(
        stock_order=Case(
            When(quantity__gt=0, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    )

    order = request.GET.get('order')

    if order in ['price', '-price', '-created_at', '-view']:
        queryset = queryset.order_by('stock_order', order)
    else:
        queryset = queryset.order_by('-chosen','stock_order' ,'-view', '-created_at' ,'title')

    start_price = request.GET.get('start_price')
    end_price = request.GET.get('end_price')

    if start_price:
        queryset = queryset.filter(price__gte=int(start_price.replace('،', '')))

    if end_price:
        queryset = queryset.filter(price__lte=int(end_price.replace('،', '')))

    brands = request.GET.getlist('brand')
    if brands:
        queryset = queryset.filter(brand_id__in=brands)

    if request.GET.get('available'):
        queryset = queryset.filter(quantity__gt=0)

    offer = request.GET.get('offer')
    if offer:
        queryset = queryset.order_by('-offer')

    return queryset.distinct()
