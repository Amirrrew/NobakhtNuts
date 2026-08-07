from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.template.base import kwarg_re
from django.core import validators

from article_module.models import Article
from home_module.models import SpecialEvents, LandingPage, Carousel
from order_module.models import PaymentMethod, Cards, PostingMethod
from product_module.models import Product, ProductCategory, ProductSubCategory, PackageSize, ProductBrand
from account_module.models import User
from site_settings.models import SiteSettings, FooterLink
from support_module.models import SupportWays, Questions


class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username' ,'password']


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['holoo_id' ,'title' ,'category' ,'brand' ,'is_byWeight' ,'packs' ,'price' ,'offer' ,'quantity' ,'desc' ,'pack_weight' ,'is_active' ,'chosen' ,'only_in_qaemshahr' ,'label' ,'label_icon']


    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )
        self.fields['is_byWeight'].required = False
        self.fields['holoo_id'].required = False
        self.fields['packs'].required = False
        self.fields['desc'].required = False
        self.fields['offer'].required = False
        self.fields['pack_weight'].required = False
        self.fields['label'].required = False
        self.fields['label_icon'].required = False



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

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title' ,'author' ,'desc' ,'banner' ,'slug' ,'content' ,'time_to_read' ,'is_active']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['banner'].required = False

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


class SupportWayForm(forms.ModelForm):
    class Meta:
        model = SupportWays
        fields = ['title' ,'name' ,'desc' ,'icon' ,'opt1' ,'opt2' ,'opt3']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['opt2'].required = False
        self.fields['opt3'].required = False


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['title' ,'email' ,'phone' ,'domain' ,'version' ,'tel' ,'is_default']

class FooterLinkForm(forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = '__all__'

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['product_category_url'].required = False
        self.fields['url'].required = False


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['title' ,'merchant_id' ,'desc' ,'is_active' ,'card']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['merchant_id'].required = False
        self.fields['card'].required = False

class CardForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields= ['title' ,'card_code' ,'owner' ,'shaba']

    def __init__(self ,*args ,**kwargs ):
        super().__init__(*args ,**kwargs )

        self.fields['shaba'].required = False


class PostingForm(forms.ModelForm):
    class Meta:
        model = PostingMethod
        fields = '__all__'


class EventForm(forms.ModelForm):
    class Meta:
        model = SpecialEvents
        fields = '__all__'

class SliderForm(forms.ModelForm):
    class Meta:
        model = LandingPage
        fields = '__all__'

class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = '__all__'

    def __init__(self ,*args ,**kwargs):
        super().__init__(*args ,**kwargs )
        self.fields['banner'].required = False
        self.fields['icon'].required = False
        self.fields['url'].required = False
        self.fields['emoji'].required = False

class FAQForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'