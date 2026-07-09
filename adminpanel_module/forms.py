from django import forms

from product_module.models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['holoo_id' ,'title' ,'category' ,'brand' ,'is_byWeight' ,'packs' ,'price' ,'offer' ,'quantity' ,'desc']