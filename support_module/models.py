from django.db import models
from django.forms import SlugField
from django.urls import reverse
from django.utils.crypto import get_random_string
from slugify import slugify

from account_module.models import User


# Create your models here.
class TicketStatus(models.Model):
    title = models.CharField(max_length=100 ,null=True,blank=False ,verbose_name='وضعیت تیکت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "وضعیت تیکت"
        verbose_name_plural = 'وضعیت تیکت ها'

class TicketReason(models.Model):
    title = models.CharField(max_length=100 ,null=True ,blank=False ,verbose_name='مشکل در')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مشکل'
        verbose_name_plural = 'مشکلات مطرح در تیکت'

class Ticket(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name="عنوان تیکت")
    status = models.ForeignKey(TicketStatus,null=True,blank=True,on_delete=models.SET_NULL,verbose_name="وضعیت")
    reason = models.ForeignKey(TicketReason,null=True,on_delete=models.SET_NULL,blank=True,verbose_name="دلیل ارسال")
    user = models.ForeignKey(User,null=True,blank=True, db_index=True,on_delete=models.CASCADE,verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True,db_index=True ,verbose_name="تاریخ ارسال")
    slug = models.SlugField(null=True,blank=True,unique=True,max_length=200,verbose_name="عنوان در url")
    is_closed = models.BooleanField(default=False, verbose_name="بسته شده؟")
    text = models.TextField(null=True,blank=True,verbose_name="متن")
    img = models.ImageField(upload_to="tickets" ,null=True ,blank=True ,verbose_name='عکس از مشکل')

    # def get_absolute_url(self):
    #     return reverse("ticket_detail", args={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "تیکت پشتیبانی"
        verbose_name_plural = "تیکت های پشتیبانی"



class SupportWays(models.Model):
    title = models.CharField(max_length=100 ,verbose_name='عنوان')
    name = models.CharField(max_length=100,null=True ,blank=True ,verbose_name='نام')
    desc = models.TextField(max_length=200,blank=True ,null=True ,verbose_name='توضیحات')
    icon = models.CharField(max_length= 1000,verbose_name='آیکون')
    opt1 = models.CharField(max_length=1000,null=True ,blank=True ,verbose_name='گزینه 1')
    opt2 = models.CharField(max_length=1000,null=True ,blank=True ,verbose_name='گزینه 1')
    opt3 = models.CharField(max_length=1000,null=True ,blank=True ,verbose_name='گزینه 1')
    banner = models.ImageField(upload_to='support_banners' ,blank=True ,null=True ,verbose_name='بنر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'راه ارتباطی'
        verbose_name_plural = 'راه های ارتباطی'

class QuestionCategory(models.Model):
    title = models.CharField(max_length=200 ,blank=True,null=True ,verbose_name='دسته بندی سوالات')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی سوال'
        verbose_name_plural = 'سوالات متداول'


class Questions(models.Model):
    category = models.ForeignKey(QuestionCategory,on_delete=models.CASCADE,related_name='question_set' ,verbose_name='در دسته')
    question = models.CharField(max_length=200 ,verbose_name='سوال')
    answer = models.TextField(max_length=2000 ,verbose_name='پاسخ به سوال')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات متداول'