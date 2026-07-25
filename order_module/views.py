import json
import os
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_image_file_extension
from django.urls import reverse
from django.utils import timezone
from itertools import product
import datetime
from django.db.models import F, prefetch_related_objects
from django.conf import settings
import requests
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View
from iranian_cities.models import Province ,City

from account_module.models import Address
from order_module.form import OrderForm
from order_module.models import Order, OrderDetail, OrderStatus, PostingMethod, PaymentMethod
from product_module.models import Product, PackageSize
from userpanel_module.form import NewAddressForm
from utils.my_decorators import permission_checker_decorator_factory, validate_image_extension


def add_to_order(request: HttpRequest):
    message = ''
    error = False
    pack_id = None
    product_id = None
    product = None
    try:
        try:
            #دریافت اطلاعات از گت
            product_id = int(request.GET.get('product_id'))
            pack_id = int(request.GET.get('pack_id'))
        except(TypeError ,ValueError) as e:
            message = 'در افزودن مححصول به سبد مشکلی پیش آمد'
            error = True

        if request.user.is_authenticated:
            pack = None

            try:
                product = Product.objects.get(id=product_id ,is_active=True ,is_deleted=False)
            except Product.DoesNotExist:
                message = 'محصول نامعتبر'
                error = True
            if pack_id:
                pack_model = PackageSize.objects.filter(id=pack_id).first()
                pack = pack_model.size
            elif not pack_id and not product.is_byWeight:
                pack = 1
            else:
                message = 'در افزودن محصول به سبد مشکلی پیش آمد'
                error = True

            # چک کردن اینکه تو سبد هست یا نه
            current_order ,created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False ,is_done=False ,user=request.user)
            if product.is_byWeight:
                current_order_detail = current_order.orderdetails_set.filter(product=product ,pack_size=pack_model).first()
            else:
                current_order_detail = current_order.orderdetails_set.filter(product=product).first()

            existing_count = current_order_detail.count if current_order_detail else 0
            new_count = existing_count + 1
            requested_amount = (new_count * pack) if product.is_byWeight else new_count

            # چک کردن اینونتوری و پوش کردن به سبد
            if product.check_inventory(requested_amount):
                if current_order_detail:
                    current_order_detail.count = F('count') + 1
                    current_order_detail.save(update_fields=['count'])
                    message = 'محصول در سبد بروزرسانی شد'
                    error = False
                else:
                    new_detail = OrderDetail(order_id=current_order.id ,product_id=product.id ,pack_size=pack_model if product.is_byWeight else None ,count=1)
                    new_detail.save()
                    message = 'محصول به سبد اضافه شد'
                    error = False

                current_order.last_change = timezone.now()
                current_order.save()
            else:
                message = 'محصول با این مقدار موجود نیست'
                error = True
        else:
            return redirect('login_page')
    except Exception as e: return JsonResponse({'message': f'{e}' ,'error': True})

    prefetch_related_objects([current_order], 'orderdetails_set')

    html = render_to_string(
        'product_module/include/product_incart.html',
        {'orders': current_order.orderdetails_set.filter(product=product),
            'product': product ,
        },
        request=request
    )

    return JsonResponse({
        'message': message,
        'html': html if html is not None else False,
        'error': error
    })

def change_order_count(request: HttpRequest):
    message = ''
    error = False
    detail_id = int(request.GET.get('detail_id'))
    type = str(request.GET.get('type'))
    page = str(request.GET.get('page'))


    if detail_id is None or type is None:
        message= 'سبد خرید پیدا نشد',
        error= True
    current_order ,created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False ,is_done=False ,user=request.user)
    order_detail = current_order.orderdetails_set.filter(id=detail_id).first()
    if order_detail is None:
        message= 'سبد خرید پیدا نشد',
        error= True

    product = order_detail.product
    order_pack_model = order_detail.pack_size
    pack = order_pack_model.size if product.is_byWeight else 1

    existing_count = order_detail.count if order_detail else 0
    new_count = existing_count + 1
    requested_amount = (new_count * pack) if product.is_byWeight else new_count

    if type == 'increase':
        if product.check_inventory(requested_amount):
            order_detail.count = F('count') + 1
            order_detail.save(update_fields=['count'])

            current_order.last_change = timezone.now()
            current_order.save()
        else:
            message = 'محصول موجود نیست'
            error = True

    elif type == 'decrease':
        if order_detail.count - 1 == 0:
            order_detail.delete()
        else:
            order_detail.count = F('count') - 1
            order_detail.save()

        current_order.last_change = timezone.now()
        current_order.save()
    else:
        message = 'درخواست نامعتبر'
        error = True

    prefetch_related_objects([current_order] ,'orderdetails_set')
    if page == 'product':
        html = render_to_string(
            'product_module/include/product_incart.html',
            {
                'orders': current_order.orderdetails_set.filter(product=product),
                'product': product,
                'insufficient_items': current_order.Check_insufficient_items()
            },
            request=request
        )
    elif page == 'basket':
        current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,                                                                                     user_id=request.user.id)
        order_summary = current_order.get_order_summary()
        html = render_to_string(
            'order_module/basket_partial.html',
            {
                'orders': current_order,
                'total_items': order_summary['total_items'],
                'total_amount': order_summary['total_amount'],
                'total_weight': order_summary['total_weight'],
                'total_amount_without_discount': order_summary['total_amount_without_discount'],
                'total_discount': int(order_summary['total_discount']),
                'insufficient_items': current_order.Check_insufficient_items()
            },
            request=request
        )

    return JsonResponse({
        'html': html,
        'error': error,
        'message': message,
        'rem': product.quantity,
    })



def my_basket(request: HttpRequest):
    if request.user.is_authenticated:
        current_order ,create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid = False ,user_id=request.user.id)
        order_summary = current_order.get_order_summary()
        related_products = Product.objects.filter(is_active=True,is_deleted=False ,quantity__gt=0).order_by('-created_at')[:10]
    else:
        return redirect('login_page')

    context = {
        'slider_title': 'جدیدترین محصولات',
        'related_products': related_products,
        'orders': current_order,
        'total_items': order_summary['total_items'],
        'total_amount': order_summary['total_amount'],
        'total_weight': order_summary['total_weight'],
        'total_amount_without_discount': order_summary['total_amount_without_discount'],
        'total_discount': int(order_summary['total_discount']),
        'insufficient_items': current_order.Check_insufficient_items()
    }
    return render(request ,'order_module/shopping_basket.html' ,context)

def delete_cart(request):
    current_order = Order.objects.prefetch_related('orderdetails_set').filter(user=request.user ,is_paid=False ,is_done=False).first()
    if current_order:
        for order in current_order.orderdetails_set.all():
            order.delete()
    return redirect('my_basket_page')


class BasketCheckout(View):
    def get(self ,request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        address_form = NewAddressForm()
        order_form = OrderForm()
        message = None
        message_e = None
        popup_open = None

        provinces = Province.objects.all()
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        order_summary = current_order.get_order_summary()
        if not current_order.orderdetails_set.all():
            return redirect('my_basket_page')
        my_address = Address.objects.filter(user=request.user)
        posting_methods = PostingMethod.objects.filter(is_active=True).order_by('order_type')

        msg = request.session.get('message')
        if msg:
            message = msg
            del request.session['message']

        context = {
            'orders': current_order,
            'my_address': my_address,
            'total_amount': order_summary['total_amount'],
            'total_items': order_summary['total_items'],
            'total_weight': order_summary['total_weight'],
            'address_form': address_form,
            'order_form': order_form,
            'message': message,
            'message_e': message_e,
            'popup_open': popup_open,
            'provinces': provinces,
            'posting_methods': posting_methods,
        }
        return render(request ,'order_module/basket_checkout.html' ,context)

    def post(self ,request):
        message = None
        message_e = None
        popup_open = None
        address_form = None
        order_form = None

        user = request.user
        provinces = Province.objects.all()
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        order_summary = current_order.get_order_summary()
        my_address = Address.objects.filter(user=request.user)
        posting_methods = PostingMethod.objects.filter(is_active=True).order_by('order_type')

        form_type = request.POST.get('form_type')

        if form_type == 'new_address':
            address_form = NewAddressForm(request.POST)
            if address_form.is_valid():
                title = address_form.cleaned_data.get('title')
                province_id = request.POST.get('province')
                city_id = request.POST.get('city')
                postal_code = address_form.cleaned_data.get('postal_code')
                number_plate = address_form.cleaned_data.get('number_plate')
                phone = address_form.cleaned_data.get('phone')
                details = address_form.cleaned_data.get('details')
                receiver = address_form.cleaned_data.get('receiver')

                province = Province.objects.filter(id=province_id).first()
                city = City.objects.filter(id=city_id).first()

                new_address = Address(
                    title=title,
                    province=province,
                    city=city,
                    postal_code=postal_code,
                    number_plate=number_plate,
                    phone=phone,
                    details=details,
                    user=user,
                    receiver=receiver,
                    is_Default=False,
                )

                new_address.save()
                request.session['message'] = 'آدرس جدید با موفقیت ثبت شد'
                return redirect('checkout_page')
            else:
                message_e = "لطفا همه فیلد هارا به درستی پر کنید"
                popup_open = True


        else:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                desc = request.POST.get('desc')
                address_id = request.POST.get('address')
                posting_id = request.POST.get('posting')

                if not posting_id:
                    message_e = 'روش ارسال را انتخاب کنید'
                elif not address_id:
                    message_e = 'آدرس خود را انتخاب یا در صورت نیاز ثبت کنید'
                else:
                    address = Address.objects.filter(id=address_id ,user=request.user).first()
                    if address:
                        address.can_delete = False
                        address.save()
                    posting = PostingMethod.objects.filter(id=posting_id).first()
                    current_order.address = address
                    current_order.desc = desc
                    current_order.posting_method = posting
                    current_order.save()

                    if current_order.Check_insufficient_items():
                        return redirect('my_basket_page')

                    return redirect('payment_page')
            else:
                message_e = 'در تکمیل سبد خرید مشکلی پیش آمده!'


        context = {
            'orders': current_order,
            'my_address': my_address,
            'total_amount': order_summary['total_amount_including_postage_fee'],
            'total_items': order_summary['total_items'],
            'total_weight': order_summary['total_weight'],
            'address_form': address_form,
            'order_form': order_form,
            'message': message,
            'message_e': message_e,
            'popup_open': popup_open,
            'provinces': provinces,
            'posting_methods': posting_methods,
        }
        return render(request ,'order_module/basket_checkout.html' ,context)


class BasketPayment(View):
    def get(self ,request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        message = None
        message_e = None
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        if not current_order.address or not current_order.posting_method:
            return redirect('checkout_page')
        order_summary = current_order.get_order_summary()
        postage_fee = current_order.postage_fee()
        payment_method = PaymentMethod.objects.order_by('-pk')

        context = {
            'orders': current_order,
            'total_amount': order_summary['total_amount_including_postage_fee'],
            'total_items': order_summary['total_items'],
            'total_weight': order_summary['total_weight'],
            'postage_fee': postage_fee,
            'payment_method': payment_method,
            'message': message,
            'message_e': message_e,
        }
        return render(request ,'order_module/basket_payment.html' ,context)

    def post(self ,request):
        message = None
        message_e = None
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        total_amount = current_order.include_postage_fee()
        total_items = current_order.total_items()
        total_weight = current_order.order_weight()
        postage_fee = current_order.postage_fee()
        payment_method = PaymentMethod.objects.all()

        pay = request.POST.get('payment')
        if pay:
            pay_method = PaymentMethod.objects.filter(id=pay).first()
            current_order.payment_method = pay_method
            current_order.save()
            if pay_method:
                if current_order.Check_insufficient_items():
                    return redirect('my_basket_page')
                else:
                    current_order.make_reservation()
                    if pay_method.id == 1:
                        return redirect('deposit_page')
                    else:
                        return request_online_payment(request)
            else:
                message_e = 'روش پرداخت نامعتبر'

        context = {
            'orders': current_order,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_weight': total_weight,
            'postage_fee': postage_fee,
            'payment_method': payment_method,
            'message': message,
            'message_e': message_e,
        }
        return render(request ,'order_module/basket_payment.html' ,context)


class Deposit(View):
    def get(self ,request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        message = None
        message_e = None
        payment_method = PaymentMethod.objects.filter(title='کارت به کارت').first()
        current_order = Order.objects.filter(user=request.user ,is_paid=False ,payment_method=payment_method).first()
        if not current_order or not current_order.stock_reserved:
            return redirect('payment_page')
        total_amount = current_order.include_postage_fee() * 10
        card = payment_method.card


        context = {
            'message': message,
            'message_e': message_e,
            'card': card,
            'payment_method': payment_method,
            'total_amount': total_amount,
        }
        return render(request ,'order_module/include/basket_deposit.html' ,context)


    def post(self ,request):
        message = None
        message_e = None
        payment_method = PaymentMethod.objects.filter(title='کارت به کارت').first()
        current_order = Order.objects.get(user=request.user ,is_paid=False ,payment_method=payment_method)
        total_amount = current_order.include_postage_fee() * 10
        card = payment_method.card

        receipt = request.FILES.get('receipt')
        if not receipt:
            message_e = 'رسید واریزی را آپلود کنید!'
        else:
            is_validate = validate_image_extension(receipt)
            if is_validate:
                try:
                    status = OrderStatus.objects.filter(title__iexact='در انتظار تایید').first()
                    address = Address.objects.filter(id=current_order.address.id).first()
                    current_order.finalize_order(receipt ,status)
                    address.can_delete = False
                    address.save()
                    self.request.session['message'] = 'سفارش با موفقیت ثبت شد'
                    return redirect(current_order.get_absolute_url())
                except:
                    message_e = 'در ثبت سفارش مشکلی پیش آمد!'
            else:
                message_e = 'فقط فایل‌های jpg، png یا webp مجاز هستند'


        context = {
            'message': message,
            'message_e': message_e,
            'card': card,
            'payment_method': payment_method,
            'total_amount': total_amount,
        }
        return render(request ,'order_module/include/basket_deposit.html' ,context)





CallbackURL = "https://nobakhtnuts.ir/orders/verify-payment/"
@login_required
def request_online_payment(request):
    errors = None
    e_code = None
    e_message = None
    online_pay_merchant = PaymentMethod.objects.filter(title='پرداخت آنلاین').first()
    try:
        current_order ,created = Order.objects.get_or_create(is_paid=False ,is_done=False ,user=request.user)
        if not current_order.stock_reserved:
            current_order.make_reservation()
        total = current_order.include_postage_fee()
        total_to_irrial = total * 10

        req_data = {
            'merchant_id': online_pay_merchant.merchant_id,
            'amount': total_to_irrial,
            'callback_url': CallbackURL,
            'description': f'برنج و خشکبار نوبخت\n پرداخت سفارش شماره {current_order.pk}',
            'metadata':{
                'mobile': str(request.user.phone)
            },
        }

        req_header = {'accept': 'application/json' ,'content-type': 'application/json'}
        response = requests.post(settings.ZP_API_REQUEST ,data=json.dumps(req_data), headers=req_header ,timeout=30)
        response_data = response.json()

        if response.status_code == 200 and 'data' in response_data:
            authority = response_data['data'].get('authority')
            if authority:
                return redirect(f'{settings.ZP_API_STARTPAY}{authority}')

            errors = response_data.get('errors', {})
            e_code = errors.get('code', 'Unknown Error')
            e_message = errors.get('message', 'Unknown message')
        return HttpResponse(f'خطا در پرداخت\n {e_code}\n {e_message}')

    except Exception as e:
        return HttpResponse(f"خطا!! {str(e)}")


def verify_payment(request: HttpRequest):
    t_authority = request.GET.get('Authority')
    online_pay_merchant = PaymentMethod.objects.filter(id=2).first()
    if request.GET.get('Status') == 'OK':
        try:
            current_order = Order.objects.get(user=request.user ,is_paid=False ,is_done=False)
        except Order.DoesNotExist:
            context = {
                'error': 'سفارش یافت نشد!',
                'returning': 'درحال بازگشت به سبد خرید',
                'redirect_url': reverse('my_basket_page'),
            }
            return render(request ,'order_module/include/payment_verify.html' ,context)

        total = current_order.include_postage_fee()
        total_to_irrial = total * 10

        req_header = {'accept': 'application/json', 'content-type': 'application/json'}
        req_data = {
            'merchant_id': online_pay_merchant.merchant_id,
            'amount': total_to_irrial,
            'authority': t_authority,
        }

        response = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        response_json = response.json()

        if len(response_json.get('errors' ,{})) == 0:
            t_status = response_json['data']['code']
            ref_id = response_json["data"]["ref_id"]
            if t_status == 100:
                status = OrderStatus.objects.filter(title__iexact='پرداخت شده').first()
                current_order.finalize_order(None ,status)
                current_order.payment_ref = ref_id
                current_order.save()
                context = {
                    'success': 'پرداخت موفق!',
                    'returning': 'در حال انتقال به صفحه سفارش های من',
                    'redirect_url': reverse('my_orders_page'),
                }
                return render(request ,'order_module/include/payment_verify.html' ,context)

            elif t_status == 101:
                context = {
                    'success': 'پرداخت قبلا انجام شده!',
                    'returning': 'در حال انتقال به صفحه سفارش های من',
                    'redirect_url': reverse('my_orders_page'),
                }
                return render(request ,'order_module/include/payment_verify.html' ,context)

            else:
                current_order.drop_reservation()
                context = {
                    'error': 'پرداخت ناموفق!',
                    'returning': 'در حال انتقال به سبد خرید',
                    'redirect_url': reverse('my_basket_page'),
                }
                return render(request ,'order_module/include/payment_verify.html' ,context)

        else:
            current_order.drop_reservation()
            context = {
                'error': 'پرداخت ناموفق!',
                'returning': 'در حال انتقال به سبد خرید',
                'redirect_url': reverse('my_basket_page'),
            }
            return render(request, 'order_module/include/payment_verify.html', context)
    else:
        current_order = Order.objects.get(user=request.user, is_paid=False)
        if current_order:
            current_order.drop_reservation()
        context = {
            'error': 'پرداخت ناموفق!',
            'returning': 'در حال انتقال به سبد خرید',
            'redirect_url': reverse('my_basket_page'),
        }

        return render(request, 'order_module/include/payment_verify.html', context)


