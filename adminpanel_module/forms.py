from django import forms

from product_module.models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = []