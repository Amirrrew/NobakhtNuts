from django.db import models

from product_module.models import Product


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


class SliderSlide(models.Model):
    title = models.CharField(max_length=100 ,null=True ,blank=False ,verbose_name='عنوان اسلاید')
    desc = models.CharField(max_length=200 ,null=True ,blank=False ,verbose_name='نوشته')
    banner = models.ImageField(upload_to='sliders', null=True ,blank=False ,verbose_name='بنر اسلاید')
    is_primary = models.BooleanField(default=False ,verbose_name='اسلاید اصلی؟')
    is_active = models.BooleanField(default=True ,verbose_name='فعال؟')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدر ها'

class Carousel(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='عنوان کاروزل کالا')
    desc = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='توضیحات')
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