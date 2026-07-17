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