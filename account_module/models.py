from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.urls import reverse
from django.utils import timezone


class BlackList_phones(models.Model):
    phone = models.CharField(max_length=1000,db_index=True ,null=True ,blank=True ,verbose_name='شماره بن شده')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'شماره بن شده'
        verbose_name_plural = 'لیست سیاه'

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars' , null=True, blank=True ,verbose_name="تصویر پروفایل")
    phone = models.CharField(max_length=11 ,blank=True,null=True,verbose_name="شماره موبایل")
    about_me = models.TextField(blank=True,null=True,verbose_name="درباره من")
    created_at = models.DateTimeField(auto_now_add=True,null=True ,verbose_name="تاریخ ثبت نام")

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

class Address(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE ,verbose_name='کاربر')
    title = models.CharField(max_length=200 ,null=True ,blank=True,verbose_name='عنوان آدرس')
    province = models.CharField(max_length= 1000 ,null=True ,blank=True ,verbose_name='استان')
    city = models.CharField(max_length=1000 ,null=True ,blank=True ,verbose_name='شهر')
    postal_code = models.CharField(max_length=10 ,null=True ,blank=True ,db_index=True ,verbose_name='کد پستی 10 رقمی')
    number_plate = models.CharField(max_length=8 ,default=0 ,null=True ,blank=True ,verbose_name='پلاک')
    details = models.CharField(max_length=1000 ,null=True ,blank=True ,verbose_name='جزئیات آدرس')
    phone = models.CharField(max_length=11 ,null=True ,blank=True ,verbose_name='شماره ثابت')
    receiver = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='نام دریافت کننده')
    is_Default = models.BooleanField(default=False ,verbose_name="آدرس پیشفرض")
    can_delete = models.BooleanField(default=True ,verbose_name='قابلیت حذف')

    def __str__(self):
        return f'{self.user.username}: {self.title}'

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

class Notification(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='عنوان پیام')
    text = models.TextField(null=True ,blank=True ,verbose_name='متن پیام')
    user = models.ForeignKey(User ,on_delete=models.CASCADE ,verbose_name='کاربر')
    is_read = models.BooleanField(default=False ,verbose_name='خوانده شده')
    is_seen = models.BooleanField(default=False ,verbose_name='دیده شده')
    created_at = models.DateTimeField(auto_now_add=True ,verbose_name='تاریخ و زمان')

    def __str__(self):
        return f'{self.user}: {self.title}'

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def get_absolute_url(self):
        return reverse('notif_detail_page' ,args=[self.pk])

    @property
    def passed_time(self):
        delta = timezone.now() - self.created_at

        if delta.days > 0:
            return f'{delta.days} روز پیش'

        hours = delta.seconds // 3600
        if hours > 0:
            return f'{hours} ساعت پیش'

        minutes = delta.seconds // 60
        if minutes > 0:
            return f'{minutes} دقیقه پیش'

        return 'لحظاتی پیش'


