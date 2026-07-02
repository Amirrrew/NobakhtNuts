from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


class NewTicketForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators = [
            MaxLengthValidator(100)
        ]
    )

    reason = forms.Select()

    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        reason = cleaned_data.get('reason')
        text = cleaned_data.get('text')

        if not title:
            raise ValidationError('عنوانی وارد کنید')
        return cleaned_data