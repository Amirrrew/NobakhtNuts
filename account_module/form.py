from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.forms import PasswordInput

from .models import User


class VerifySignupForm(forms.Form):
    verify_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators = [
            validators.MaxLengthValidator(6),
            validators.MinLengthValidator(6),
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        verify_code = cleaned_data.get('verify_code')
        if not verify_code:
            raise ValidationError('کد تایید را وارد کنید')
        return cleaned_data


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators = [
            validators.MaxLengthValidator(11),
            validators.MinLengthValidator(11),
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError('شماره تلفن خود را وارد کنید')

        return cleaned_data




class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators= [
            MinLengthValidator(8)
        ]
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators = [
            MinLengthValidator(8)
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if confirm_password != password:
            raise ValidationError('پسورد ها با هم مطابقت ندارند')
        return cleaned_data