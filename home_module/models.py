from django.db import models

from product_module.models import Product, ProductCategory, ProductSubCategory


class SpecialEvents(models.Model):
    title = models.CharField(max_length=100 ,null=True ,blank=False ,verbose_name='عنوان رویداد')
    desc = models.CharField(max_length=50 ,null=True ,blank=False ,verbose_name='توضیح کوتاه')
    emoji = models.CharField(max_length=2 ,null=True ,blank=False ,verbose_name='ایموجی')
    url = models.CharField(max_length=1000 ,null=True ,blank=False ,verbose_name='url')
    is_active = models.BooleanField(default=False ,verbose_name='نمایش')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رویداد'
        verbose_name_plural = 'رویداد ها'


class LandingPage(models.Model):
    pill_text = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='نوشته pill-bar')
    text = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='نوشته اصلی')
    desc = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='نوشته کوچک')
    banner = models.ImageField(upload_to='sliders', null=True ,blank=False ,verbose_name='بنر اسلاید')
    url = models.CharField(max_length=1000 ,null=True ,blank=False ,verbose_name='url اسلایدر')
    is_active = models.BooleanField(default=True ,verbose_name='فعال؟')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'لندینگ پیج'
        verbose_name_plural = 'لندینگ پیج ها'


class Carousel(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=False ,verbose_name='عنوان کاروزل کالا')
    desc = models.CharField(max_length=200 ,null=True ,blank=False ,verbose_name='توضیحات')
    banner = models.ImageField(upload_to='carousels' ,null=True ,blank=True ,verbose_name='بنر')
    is_active = models.BooleanField(default=False ,db_index=True ,verbose_name='فعال / غیرفعال')
    url = models.CharField(max_length= 1000 ,null=True ,blank=True ,verbose_name='آدرس در صورت نیاز')
    icon = models.CharField(max_length= 2000 ,null=True ,blank=True ,verbose_name='آیکون')
    emoji = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='ایموجی')
    color_bg = models.CharField(max_length=100 ,null=True ,blank=True, default='#fff' ,verbose_name='رنگ قالب')
    color_fore = models.CharField(max_length=100 ,null=True ,blank=True, default='#fff' ,verbose_name='رنگ متن')
    switch_on_break = models.BooleanField(db_index=True ,default=False ,verbose_name='سوییچ به رنگ قالب در موبایل')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کاروزل'
        verbose_name_plural = 'کاروزل ها'

class CarouselItem(models.Model):
    carousel = models.ForeignKey(Carousel,on_delete=models.CASCADE ,null=False ,blank=False,related_name='carousel_set' ,verbose_name='زیر مجموعه کاروزل؟')
    product = models.ForeignKey(Product,on_delete=models.CASCADE ,db_index=True ,null=False ,blank=False ,verbose_name='کالا')

    def __str__(self):
        return f'{self.carousel}-item-{self.pk}'

    class Meta:
        verbose_name= 'آیتم کاروزل'
        verbose_name_plural = 'آیتم های کاروزل'


class CardBlock(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=False ,verbose_name='بلاک کارت ها')
    seo_name = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='اسم برای سئو(درصورت نیاز)')
    icon = models.ImageField(upload_to='cards_block' ,null=True ,blank=False ,verbose_name='آیکون')
    url_category = models.ForeignKey(ProductCategory,null=True ,blank=True,on_delete=models.CASCADE ,verbose_name='مرتبط با دسته')
    is_active = models.BooleanField(default=True ,db_index=True ,verbose_name='فعال؟')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بلاک کارت ها'


class HomeCards(models.Model):
    card_block = models.ForeignKey(CardBlock,on_delete=models.CASCADE ,db_index=True ,null=False ,blank=False,related_name='cardblock_set' ,verbose_name='بلاک کارت ها')
    category = models.ForeignKey(ProductSubCategory ,on_delete=models.CASCADE ,db_index=True ,null=False ,blank=False ,verbose_name='مرتبط با دسته')
    cover = models.ImageField(upload_to='card_images' ,null=True ,blank=False ,db_index=True ,verbose_name='تصویر')

    def __str__(self):
        return f'{self.card_block.title}: {self.category.title}'


class Banner(models.Model):
    title = models.CharField(max_length=100 ,null=False ,blank=False ,verbose_name='عنوان')
    seo_name = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='نام برای سئو')
    category = models.ForeignKey(ProductCategory ,on_delete=models.CASCADE ,db_index=True ,null=True ,blank=True ,verbose_name='مربوط به شاخه اصلی؟')
    sub_category = models.ForeignKey(ProductSubCategory ,on_delete=models.CASCADE ,db_index=True ,null=True ,blank=True ,verbose_name='مربوط به زیرشاخه؟')
    url = models.CharField(max_length=1000 ,null=True ,blank=True ,verbose_name='آدرس url')
    image = models.ImageField(upload_to='home_banner' ,null=False ,blank=False ,verbose_name='تصویر')
    desc = models.TextField(max_length=100 ,null=True ,blank=True ,verbose_name='توضیحات (درصورت نیاز)')
    is_active = models.BooleanField(default=True ,db_index=True ,verbose_name="فعال؟")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر صفحه اصلی'
        verbose_name_plural = 'بنر های صفحه اصلی'