from django import forms
from django.core.exceptions import ValidationError

from product_module.models import ProductComment


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text' ,'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     text = cleaned_data.get('text')
    #     rating = cleaned_data.get('rating')
    #     if text and rating:
    #         raise ValidationError('تمامی فیلد هارا پر کنید')
