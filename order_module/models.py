from datetime import datetime
from itertools import product

from django.utils import timezone

from django.db import models ,transaction
from django.db.models import DO_NOTHING, Sum
from django.template.defaultfilters import default
from django.urls import reverse
from urllib3 import request

from account_module.models import User, Address
from product_module.models import Product, PackageSize



class PostingMethod(models.Model):
    title = models.CharField(max_length=100 ,null=True ,verbose_name='روش ارسال')
    price_range = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='محدوده قیمتی')
    price_single = models.IntegerField(verbose_name='نرخ معمولی')
    price_per_k = models.PositiveIntegerField(verbose_name='نرخ بر کیلو')
    tax = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='ارزش افزوده')
    max_weight = models.FloatField(max_length=100,null=True ,blank=True ,verbose_name='محدوده وزنی')
    is_active = models.BooleanField(default=True,db_index=True ,verbose_name='فعال / غیر فعال')
    time = models.CharField(max_length=200,null=True ,blank=True ,verbose_name='زمان ارسال')
    estimated_time = models.PositiveIntegerField(default=0 ,null=True ,blank=True ,verbose_name='زمان برای ارسال به عدد')
    desc = models.TextField(max_length=1000,null=True ,blank=True ,verbose_name='توضیحات')
    order_type = models.PositiveIntegerField(null=True ,blank=True ,verbose_name='ترتیب')
    icon = models.CharField(max_length= 1000,null=True ,blank=True ,verbose_name='آیکون')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'روش ارسال'
        verbose_name_plural = 'روش های ارسال'



class Cards(models.Model):
    title = models.CharField(max_length=100 ,verbose_name='کارت')
    card_code = models.CharField(max_length=16 ,verbose_name='شماره کارت')
    shaba = models.CharField(max_length=26 ,null=True ,blank=True ,verbose_name='شماره شبا با IR')
    owner = models.CharField(max_length=100 ,null=True ,blank=True ,verbose_name='به نام')
    is_active = models.BooleanField(default=True,db_index=True ,verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کارت'
        verbose_name_plural = 'کارت ها'


class OrderStatus(models.Model):
    title = models.CharField(max_length=100,db_index=True ,verbose_name='وضعیت سفارش')
    progress_level = models.IntegerField(null=True ,blank=True ,verbose_name='میزان پیشرفت به درصد')
    icon = models.TextField(null=True ,blank=True ,verbose_name='آیکون')
    desc = models.TextField(null=True ,blank=True ,verbose_name='توضیحات')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'وضعیت های سفارش'


class PaymentMethod(models.Model):
    title = models.CharField(max_length=100 ,null=True ,verbose_name='روش پرداخت')
    card = models.ForeignKey(Cards,null=True ,blank=True ,on_delete=models.DO_NOTHING ,verbose_name='کارت')
    desc = models.TextField(max_length=500 ,null=True ,blank=True ,verbose_name='توضیحات')
    steps = models.ManyToManyField(OrderStatus ,null=True ,blank=True ,verbose_name='مراحل')
    merchant_id = models.CharField(max_length= 2000,null=True ,blank=True ,verbose_name='مرچنت آیدی')
    is_active = models.BooleanField(default=True,db_index=True ,verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'روش پرداخت'
        verbose_name_plural = 'روش های پرداخت'


class Order(models.Model):
    user = models.ForeignKey(User, db_index=True,on_delete=models.CASCADE ,verbose_name='کاربر')
    is_paid = models.BooleanField(default=False,db_index=True ,verbose_name='پرداخت شده')
    is_done = models.BooleanField(default=False,db_index=True ,verbose_name='پایان یافته')
    payment_date = models.DateTimeField(db_index=True,null=True ,blank=True ,verbose_name='تاریخ پرداخت')
    status = models.ForeignKey(OrderStatus,db_index=True,on_delete=DO_NOTHING ,null=True ,blank=True ,verbose_name='وضعیت')
    desc = models.TextField(max_length=3000 ,null=True ,blank=True ,verbose_name='توضیحات سفارش')
    address = models.ForeignKey(Address ,on_delete=DO_NOTHING ,null=True ,blank=True ,verbose_name='آدرس')
    payment_method = models.ForeignKey(PaymentMethod,on_delete=DO_NOTHING ,null=True ,blank=True ,verbose_name='روش پرداخت')
    posting_method = models.ForeignKey(PostingMethod ,on_delete=DO_NOTHING ,null=True ,blank=True ,verbose_name='روش ارسال')
    receipt = models.ImageField(upload_to='receipts' ,null=True ,blank=True ,verbose_name='رسید واریزی')
    finalized_price = models.IntegerField(null=True ,blank=True ,verbose_name='قیمت نهایی')
    postage_fee = models.IntegerField(null=True ,blank=True ,verbose_name='هزینه ارسال')
    payment_ref = models.CharField(max_length=200 ,null=True ,blank=True ,verbose_name='شماره تراکنش')
    last_change = models.DateTimeField(null=True ,blank=True ,verbose_name='آخرین تغییرات')
    stock_reserved = models.BooleanField(default=False ,verbose_name='موجودی رزرو شده؟')
    stock_reservation_time = models.DateTimeField(blank=True ,null=True ,verbose_name='زمان رزرو موجودی')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self ,*args):
        return reverse('order_detail_page' ,args=[self.pk])

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید کاربران'
        indexes = [
            models.Index(fields=['user','status','is_paid', 'is_done', 'payment_date'], name='idx_order_pending_close'),
        ]

    def calculate_total_price(self):
        total = 0
        for detail in self.orderdetails_set.all():
            total += detail.total_price
        return total

    def total_items(self):
        return self.orderdetails_set.aggregate(total=Sum('count'))['total'] or 0

    def order_weight(self):
        weight = float(0)
        for detail in self.orderdetails_set.all():
            weight+=detail.calculate_package_weight
        return weight

    @transaction.atomic
    def make_reservation(self, *args ,**kwargs):
        details = self.orderdetails_set.select_related('product' ,'pack_size')
        for detail in details:
            detail.product.shop(detail.count , detail.pack_size.size if detail.pack_size is not None else 1)

        self.stock_reserved = True
        self.stock_reservation_time = timezone.now()
        self.save(update_fields=['stock_reserved', 'stock_reservation_time'])

    @transaction.atomic
    def drop_reservation(self):
        details = self.orderdetails_set.select_related('product' ,'pack_size')
        for detail in details:
            detail.product.q_back(detail.count ,detail.pack_size.size if detail.pack_size and detail.product.is_byWeight else 1)
        self.stock_reserved = False
        self.stock_reservation_time = None
        self.save(update_fields=['stock_reserved', 'stock_reservation_time'])

    def get_order_summary(self):
        details = self.orderdetails_set.select_related('product', 'pack_size')

        total_amount = 0
        total_items = self.total_items()
        total_weight = float(0)
        total_discount = int(0)
        total_amount_without_discount = 0

        for detail in details:
            total_amount += detail.total_price
            total_amount_without_discount += detail.total_price_without_discount
            total_weight += detail.calculate_package_weight
            total_discount+= detail.discount_amount

        total_amount_including_postage_fee = total_amount + self.postage_fee()

        return {
            'total_amount': total_amount,
            'total_items': total_items,
            'total_weight': total_weight,
            'total_discount': total_discount,
            'total_amount_without_discount': total_amount_without_discount,
            'total_amount_including_postage_fee': total_amount_including_postage_fee
        }

    def postage_fee(self):
        weight = self.order_weight()
        if self.posting_method.title == 'پست پیشتاز':
            if weight <= 1:
                return int(self.posting_method.price_single)
            else:
                return int(self.posting_method.price_per_k * weight) + int(self.posting_method.tax)
        else:
            return 0

    def total_discount(self):
        details = self.orderdetails_set.select_related('product', 'pack_size')
        total_discount = int(0)
        for detail in details:
            total_discount += detail.discount_amount
        return total_discount


    def include_postage_fee(self):
        return self.calculate_total_price() + self.postage_fee()

    @property
    def order_progress(self):
        status = self.status.title

        if status == 'در انتظار تایید' or status == 'پرداخت شده':
            progress = 25
        elif status == 'در حال آماده سازی':
            progress = 50
        elif status == 'ارسال شده':
            progress = 75
        elif status == 'پایان یافته':
            progress = 100
        else:
            progress = 0

        return progress

    def Check_insufficient_items(self):
        order_details = self.orderdetails_set.select_related('product', 'pack_size')
        insufficient_items = [d for d in order_details if not d.Check_product_inventory()]
        return insufficient_items

    def finalize_order(self ,receipt ,status):
        self.receipt = receipt
        self.status = status
        self.is_paid = True
        self.payment_date = timezone.now()
        self.finalized_price = self.include_postage_fee()
        self.postage_fee = self.postage_fee()
        for detail in self.orderdetails_set.all():
            detail.final_price = detail.total_price
            detail.save()
        self.save()

    def approve_order(self):
        self.status = OrderStatus.objects.filter(title__iexact='در حال آماده سازی').first()
        self.save()

    def send_order(self):
        self.status = OrderStatus.objects.filter(title__iexact='ارسال شده').first()
        self.save()

    def reject_order(self):
        self.status = OrderStatus.objects.filter(title__iexact='رد شده').first()
        self.save()

    def return_order(self):
        for o in self.orderdetails_set.all():
            if o.product.is_byWeight:
                o.product.q_back(o.count, o.pack_size.size)
            else:
                o.product.q_back(o.count, 1)
        self.is_done = True
        self.status = OrderStatus.objects.filter(title__iexact="مرجوع شده").first()
        self.save()




class OrderDetail(models.Model):
    order = models.ForeignKey(Order,db_index=True ,on_delete=models.CASCADE ,verbose_name='جزئیات سفارش' ,related_name='orderdetails_set')
    product = models.ForeignKey(Product,db_index=True ,on_delete=models.CASCADE ,verbose_name='محصول')
    pack_size = models.ForeignKey(PackageSize,db_index=True,null=True ,blank=True ,on_delete=models.CASCADE ,verbose_name='اندازه بسته بندی')
    count = models.PositiveIntegerField(null=True ,blank=True ,verbose_name='تعداد')
    final_price = models.IntegerField(null=True ,blank=True ,verbose_name='قیمت نهایی')
    insufficient = models.BooleanField(null=True ,default=False ,blank=True ,db_index=True ,verbose_name='آیتم کافی؟')

    def __str__(self):
        return str(self.order.id)

    @property
    def unit_price(self):
        if self.product.is_byWeight:
            return int(self.product.final_price * self.pack_size.size)
        return self.product.final_price

    @property
    def total_price(self):
        return self.unit_price * self.count

    @property
    def total_price_without_discount(self):
        if self.product.is_byWeight:
            return int(self.product.price * self.pack_size.size) * self.count
        return self.product.price * self.count

    @property
    def calculate_package_weight(self):
        weight = float(0)
        if self.product.is_byWeight:
            weight = self.pack_size.size * self.count
        else:
            if self.product.pack_weight:
                weight = self.product.pack_weight * self.count
        return weight

    def Check_product_inventory(self):
        return self.product.quantity - (self.count * self.pack_size.size) >=0 if self.product.is_byWeight else self.product.quantity - self.count >= 0

    @property
    def discount_amount(self):
        return (self.product.price * self.product.offer // 100) * self.count if not self.product.is_byWeight else (self.product.price * self.product.offer // 100) * (self.count * self.pack_size.size)



