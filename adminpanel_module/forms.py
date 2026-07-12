from django import forms

from product_module.models import Product, ProductCategory, ProductSubCategory, PackageSize, ProductBrand
from account_module.models import User


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


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['title' ,'slug' ,'is_active' ,'emoji' ,'column']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['slug'].required = True


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductSubCategory
        fields = ['title' ,'slug' ,'main_category' ,'is_active']

class PackForm(forms.ModelForm):
    class Meta:
        model = PackageSize
        fields = '__all__'

class BrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['title' ,'slug' ,'logo' ,'is_active']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone' ,'first_name' ,'last_name' ,'email' ,'username' ,'about_me']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )
        self.fields['about_me'].required = False
        self.fields['last_name'].required = False
        self.fields['first_name'].required = False
        self.fields['email'].required = False
        self.fields['username'].required = False
