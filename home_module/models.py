from django.db import models

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