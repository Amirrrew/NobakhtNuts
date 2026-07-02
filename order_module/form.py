from django import forms
from django.core.exceptions import ValidationError

from order_module.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['desc', 'address', 'posting_method']