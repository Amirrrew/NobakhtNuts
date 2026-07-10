from django import forms

from product_module.models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['holoo_id' ,'title' ,'category' ,'brand' ,'is_byWeight' ,'packs' ,'price' ,'offer' ,'quantity' ,'desc' ,'pack_weight' ,'is_active']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )
        self.fields['is_byWeight'].required = False
        self.fields['holoo_id'].required = False
        self.fields['packs'].required = False
        self.fields['desc'].required = False
        self.fields['offer'].required = False
        self.fields['pack_weight'].required = False
