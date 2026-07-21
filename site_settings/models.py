from django.db import models

from product_module.models import ProductCategory


class SiteSettings(models.Model):
    title = models.CharField(max_length=100 ,verbose_name="تنظیمات")
    version = models.CharField(max_length=20 ,null=True ,blank=True ,verbose_name='ورژن سایت')
    domain = models.CharField(max_length= 300 ,verbose_name='دامنه سایت')
    url = models.CharField(max_length=300,null=True ,blank=True ,verbose_name="آدرس سایت")
    email = models.CharField(max_length=500 ,verbose_name='ایمیل سایت')
    tel = models.CharField(max_length=11 ,verbose_name='تلفن ثابت')
    phone = models.CharField(max_length=11 ,verbose_name="موبایل")
    is_default = models.BooleanField(default=False ,verbose_name="تنظیمات اصلی ؟")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات سایت'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200 ,verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی فوتر لینک'
        verbose_name_plural = 'دسته بتدی های فوتر لینک'

class FooterLink(models.Model):
    Ftitle = models.CharField(max_length=200 ,verbose_name='عنوان فوتر لینک')
    url = models.CharField(max_length=200,null=True ,blank=True ,verbose_name='آدرس')
    product_category_url = models.ForeignKey(ProductCategory,null=True ,blank=True ,on_delete=models.CASCADE ,verbose_name='دسته بندی دارای لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox ,on_delete=models.CASCADE ,verbose_name='دسته بندی' ,related_name='links')

    def __str__(self):
        return self.Ftitle

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'
