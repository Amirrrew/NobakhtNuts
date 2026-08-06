import math
from datetime import timezone
from itertools import product

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.admin import display
from django.db import models ,transaction
from django.db.models import DO_NOTHING
from django.forms import IntegerField
from django.template.context_processors import request
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify, default
from django.db.models import Avg ,F
from django.utils.timesince import timesince
from django.utils import timezone
from pyexpat.errors import messages

from account_module.models import User

class ProductCategory(models.Model):
    title = models.CharField(max_length=100 ,verbose_name="عنوان دسته بندی")
    image = models.ImageField(upload_to='category_imgs/' ,blank=True,null=True ,verbose_name="عکس دسته بندی")
    slug = models.SlugField(max_length=1000 ,default='' ,null=True ,blank=True,unique=True,db_index=True ,verbose_name="عنوان در url")
    on_delete = models.CASCADE
    is_active = models.BooleanField(default=True ,verbose_name="فعال / غیر فعال")
    emoji = models.CharField(max_length=50,null=True ,verbose_name='ایموجی')
    column = models.PositiveIntegerField(max_length=10 ,null=True ,verbose_name='ستون')

    def get_absolute_url(self):
        return reverse(
            "products_by_category",
            kwargs={
                "category": self.slug
            }
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "شاخه اصلی"
        verbose_name_plural = "شاخه های اصلی"


class ProductSubCategory(models.Model):
    main_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE ,verbose_name="شاخه اصلی" ,related_name='subcategory')
    title = models.CharField(max_length=100, verbose_name="عنوان زیرشاخه")
    image = models.ImageField(upload_to='subcategory_imgs', blank=True, null=True, verbose_name="عکس زیر شاخه")
    slug = models.SlugField(max_length=1000 ,default='' ,null=True ,blank=True,unique=True,db_index=True ,verbose_name="عنوان در url")
    is_active = models.BooleanField(default=True ,verbose_name="فعال / غیر فعال")

    def get_absolute_url(self):
        return reverse(
            "products_by_subcategory",
            kwargs={
                "subcategory": self.slug
            }
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "شاخه فرعی"
        verbose_name_plural = "شاخه های فرعی"


class ProductBrand(models.Model):
    title = models.CharField(max_length=100 ,verbose_name="عنوان برند")
    slug = models.SlugField(max_length=1000 ,default='' ,null=True ,blank=True,unique=True,db_index=True ,verbose_name="عنوان در url")
    logo = models.ImageField(upload_to='brand_logo' ,blank=True,null=True ,verbose_name="لوگو برند")
    category = models.ManyToManyField(ProductSubCategory ,null=True ,blank=True ,verbose_name='برند در حوزه')
    is_active = models.BooleanField(default=True ,verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

class PackageSize(models.Model):
    title = models.CharField(max_length=200 ,verbose_name='بسته بندی')
    size = models.FloatField(null=True ,verbose_name='وزن')
    icon = models.ImageField(upload_to='pack_sizes' ,null=True ,blank=True ,verbose_name='آیکون')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بسته بندی'
        verbose_name_plural = 'بسته بندی ها'

    def calculate_price(self, price):
        return int(price * self.size)



class Product(models.Model):
    holoo_id = models.CharField(max_length=100 ,blank=True ,null=True ,verbose_name='بارکد هلو')
    title = models.CharField(max_length=300,db_index=True ,blank=False ,null=True ,verbose_name="عنوان محصول")
    category = models.ForeignKey(ProductSubCategory,db_index=True,on_delete=models.CASCADE,null=False,blank=False,related_name='products' ,verbose_name="دسته بندی")
    brand = models.ForeignKey(ProductBrand,db_index=True ,on_delete=models.CASCADE,null=True,blank=True ,verbose_name="برند")
    price = models.IntegerField(default=0,blank=True ,null=True ,verbose_name="قیمت")
    is_byWeight = models.BooleanField(default=False ,verbose_name='کالای وزنی؟')
    quantity = models.FloatField(default=0 ,verbose_name="تعداد")
    desc = models.TextField(max_length=500000 ,null=True, blank=True ,verbose_name='توضیحات')
    user = models.ForeignKey(User ,null=True ,blank=True,on_delete=models.DO_NOTHING ,verbose_name="افزوده شده توسط کاربر")
    offer = models.IntegerField(default=0,blank=True ,null=True,db_index=True ,verbose_name="تخفیف")
    is_active = models.BooleanField(default=True,db_index=True ,verbose_name="فعال / غیر فعال")
    is_deleted = models.BooleanField(default=False,db_index=True ,verbose_name="حذف شده / نشده")
    view = models.PositiveIntegerField(default=0 ,verbose_name= 'بازدید')
    created_at = models.DateTimeField(auto_now_add=True ,db_index=True,verbose_name="تاریخ ثبت")
    slug = models.SlugField(max_length=1000 ,default='' ,null=True ,blank=True,unique=True,db_index=True ,verbose_name="عنوان در url")
    packs = models.ManyToManyField(PackageSize ,null=True ,blank=True ,verbose_name='اندازه بسته بندی های محصول')
    pack_weight = models.FloatField(null=True ,blank=True ,verbose_name='وزن بسته')
    label_icon = models.CharField(max_length=2000 ,null=True ,blank=True ,verbose_name='آیکون برای لیبل')
    label = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='لیبل کالا برای کارت محصول')
    chosen = models.BooleanField(default=False,db_index=True ,verbose_name='محصول برگزیده')
    only_in_qaemshahr = models.BooleanField(default=False ,db_index=True ,verbose_name='فقط در قائمشهر')




    def get_absolute_url(self):
        return reverse('product_detail_page' ,args=[self.slug])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'nnp-{slugify(self.title)}{get_random_string(10)}'

        super().save(*args, **kwargs)


    def __str__(self ,*args, **kwargs):
        return self.title


    @property
    def is_available(self):
        return self.quantity > 0

    @property
    def comments_count(self):
        return self.comment_set.count()

    @property
    def average_rating(self):
        avg = self.comment_set.aggregate(avg=Avg('rating'))['avg']
        return round(avg or 0, 1)

    @property
    def final_price(self):
        if self.offer and self.offer > 0:
            return self.price - (self.price * self.offer // 100)
        else:
            return self.price

    def check_inventory(self, size):
        return self.quantity - float(size) >= 0 if self.is_byWeight else self.quantity - size >= 0

    def check_total_inventory_cart(self ,total):
        return self.quantity - total

    def shop(self,count ,size ,*args ,**kwargs):
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.pk)
            deduction = (count * size) if product.is_byWeight else count

            if product.quantity - deduction < 0:
                return False

            else:
                product.quantity = F('quantity') - deduction
                product.save(update_fields=['quantity'])
                self.refresh_from_db(fields=['quantity'])
                return True

    def q_back(self, count, size):
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.pk)
            product.quantity = F('quantity') + (count * size)
            product.save(update_fields=['quantity'])


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

        indexes = [
            models.Index(
                fields=["is_active", "is_deleted", "chosen", "quantity" ,'view' ,'title'],
                name="product_listing_idx",
            ),
            models.Index(
                fields=["is_active", "is_deleted", "offer"],
                name="product_offer_idx",
            ),
        ]



class ProductImage(models.Model):
    product = models.ForeignKey(Product,db_index=True ,on_delete=models.CASCADE ,related_name='product_image')
    image = models.ImageField(upload_to='product_imgs' ,verbose_name='تصویر کالا')
    is_Main = models.BooleanField(default=False,db_index=True ,verbose_name='عکس اصلی؟')

    class Meta:
        verbose_name = 'عکس کالا'
        verbose_name_plural = 'عکس های کالا'




class ProductFeature(models.Model):
    title = models.CharField(max_length=50 ,null=True ,verbose_name='عنوان ویژگی')
    desc = models.CharField(max_length=200 ,verbose_name='توضیحات')
    product = models.ForeignKey(Product,db_index=True ,on_delete=models.CASCADE ,related_name='features' ,verbose_name='محصول')

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی ها محصول'



class ProductComment(models.Model):
    user = models.ForeignKey(User,db_index=True ,on_delete=models.CASCADE ,null=True)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE ,related_name='comment_set' ,verbose_name='برای محصول')
    text = models.TextField(max_length=2000 ,verbose_name='متن نظر')
    rating = models.FloatField(default=0 ,verbose_name='امتیاز')
    is_approved = models.BooleanField(default=False ,verbose_name='تایید شده؟')
    created_at = models.DateTimeField(auto_now_add=True,db_index=True ,verbose_name='تاریخ')
    like = models.ManyToManyField(User,db_index=True ,blank=True,null=True,related_name='likes' ,verbose_name= 'لایک')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

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

    def is_liked(self ,user):
        return self.like.filter(id=user.id).exists()





