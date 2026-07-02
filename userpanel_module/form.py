from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import TextField
from django.dispatch import receiver

from account_module.models import User

class EditInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' ,'first_name' ,'last_name' ,'about_me' ,'avatar']
        widgets ={
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.TextInput(attrs={'class': 'form-control', 'id': 'message', 'rows': 6}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ResetPasswordFormPanel(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password' ,'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords must match")

        return cleaned_data


class NewAddressForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) ,validators= [MaxLengthValidator(200) ,MinLengthValidator(2)])
    province = forms.Select(attrs={'class': 'form-control'})
    city = forms.Select(attrs={'class': 'form-control'})
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) ,validators=[MaxLengthValidator(10) ,MinLengthValidator(10)])
    receiver = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) ,validators=[MaxLengthValidator(200) ,MinLengthValidator(2)])
    number_plate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) ,validators=[MaxLengthValidator(10) ,MinLengthValidator(1)])
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) ,validators=[MaxLengthValidator(11) ,MinLengthValidator(11)])

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        province = cleaned_data.get("province")
        city = cleaned_data.get("city")
        receiver = cleaned_data.get('receiver')
        postal_code = cleaned_data.get("postal_code")
        number_plate = cleaned_data.get("number_plate")
        details = cleaned_data.get("details")
        phone = cleaned_data.get("phone")

        if not title:
            raise ValidationError('یک عنوان برای آدرس وارد کنید')
        if not postal_code:
            raise ValidationError('کد پستی اجباری است')
        if not number_plate:
            raise ValidationError('پلاک اجباری است')
        if not details:
            raise ValidationError('جزئیات آدرس را وارد کنید')
        if not phone:
            raise ValidationError('شماره تلفن را وارد کنید')
        if not receiver:
            raise ValidationError('نام دریافت کننده را وارد کنید')

        return cleaned_data


