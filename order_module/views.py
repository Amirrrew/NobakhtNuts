import json
import os
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_image_file_extension
from django.urls import reverse
from django.utils import timezone
from itertools import product
import datetime
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
from utils.my_decorators import permision_checker_decorator_factory, validate_image_extension


def add_to_order(request: HttpRequest):
    try:
        try:
            pack_id = None
            product_id = int(request.GET.get('product_id'))
        except(TypeError ,ValueError) as e:
            return JsonResponse({
                'message': f'{e}'
            }, status=400)



        if request.user.is_authenticated:
            try:
                product = Product.objects.get(id=product_id ,is_active=True ,is_deleted=False)
                count = 1
                if product.is_byWeight:
                    try:
                        pack_id = int(request.GET.get('pack'))
                    except Exception as e:
                        return JsonResponse({
                            'message': f'{e}'
                        }, status=400)
                    pack = PackageSize.objects.filter(id=pack_id).first()
                    if count * pack.size > product.quantity:
                        return JsonResponse({
                            'message': 'محصول با این مقدار موجود نیست'
                        }, status=400)
                else:
                    if count > product.quantity:
                        return JsonResponse({
                            'message': 'محصول با این مقدار موجود نیست'
                        }, status=400)

            except Product.DoesNotExist:
                return JsonResponse({
                    'message': 'محصول نامعتبر'
                }, status=400)

            status = OrderStatus.objects.filter(id=1).first()
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            if product.is_byWeight:
                current_order_detail = current_order.orderdetails_set.filter(product_id=product_id,pack_size_id=pack_id).first()
            else:
                current_order_detail = current_order.orderdetails_set.filter(product_id=product_id ,pack_size=product.packs.first()).first()

            if product.is_byWeight:
                pack = PackageSize.objects.filter(id=pack_id).first()

            if current_order_detail:
                if product.is_byWeight:
                    if product.can_shop(count, pack.size):
                        product.shop(count, pack.size)
                        current_order_detail.count += count
                        current_order_detail.save()
                        current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(
                            is_paid=False, user_id=request.user.id)
                        html = render_to_string(
                            'product_module/include/product_incart.html',
                            {
                                'orders': current_order.orderdetails_set.filter(
                                    product=product
                                ),
                                'product': product,
                            },
                            request=request
                        )
                        return JsonResponse({
                            'message': 'محصول به سبد خرید اضافه شد',
                            'html': html,
                            'error': False
                        })
                    else:
                        return JsonResponse({
                            'message': 'محصول به این مقدار موجود نیست',
                            'error': True
                        })

                else:
                    if product.can_shop(count, 1):
                        product.shop(count, 1)
                        current_order_detail.count += count
                        current_order_detail.save()
                        current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(
                        is_paid=False, user_id=request.user.id)
                        html = render_to_string(
                            'product_module/include/product_incart.html',
                            {
                                'orders': current_order.orderdetails_set.filter(
                                    product=product
                                ),
                                'product': product,
                            },
                            request=request
                        )
                        return JsonResponse({
                            'message': 'محصول به سبد خرید اضافه شد',
                            'html': html,
                            'error': False
                        })
                    else:
                        return JsonResponse({
                            'message': 'محصول به این مقدار موجود نیست',
                            'error': True
                        })
            else:
                if product.is_byWeight:
                    if product.can_shop(count, pack.size):
                        product.shop(count, pack.size)
                        new_detail = OrderDetail(order_id=current_order.id ,product_id=product_id ,pack_size=pack ,count=count)
                        current_order.status = status
                        current_order.save()
                        new_detail.save()
                else:
                    if product.can_shop(count, 1):
                        product.shop(count, 1)
                        new_detail = OrderDetail(order_id=current_order.id ,product_id=product_id ,pack_size=product.packs.first() ,count=count)
                        current_order.status = status
                        current_order.save()
                        new_detail.save()
                current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
                html = render_to_string(
                    'product_module/include/product_incart.html',
                    {
                        'orders': current_order.orderdetails_set.filter(
                            product=product
                        ),
                        'product': product,
                    },
                    request=request
                )
                return JsonResponse({
                    'message': 'محصول به سبد خرید اضافه شد',
                    'html': html,
                    'error': False
                })

        else:
            return JsonResponse({
                'message': 'برای افزودن به سبد ابتدا وارد حساب کاربری خود شوید',
                'error': True
            })



    except Exception as e:
        return JsonResponse({
            'message': f'{e}',
            'error': True
        })



def change_order_count(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    type = str(request.GET.get('type'))

    if detail_id is None or type is None:
        return JsonResponse({
            'message': 'خطای ناشناخته',
            'error': True
        })
    order_detail = OrderDetail.objects.filter(id=detail_id ,order__is_paid=False ,order__user=request.user).first()
    if order_detail is None:
        return JsonResponse({
            'message': 'جزئیات پیدا نشد',
            'error': True
        })

    product = order_detail.product

    if type == 'increase':
        if product.is_byWeight:
            pack = order_detail.pack_size.size
            if product.can_shop(1 , pack):
                product.shop(1 , pack)
                order_detail.count += 1
                order_detail.save()
            else:
                current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
                html = render_to_string(
                    'product_module/include/product_incart.html',
                    {
                        'orders': current_order.orderdetails_set.filter(
                            product=product
                        ),
                        'product': product,
                    },
                    request=request
                )
                return JsonResponse({
                    'message': 'محصول موجود نیست',
                    'error': True,
                    'html': html
                })
        else:
            if product.can_shop(1 , 1):
                product.shop(1 , 1)
                order_detail.count += 1
                order_detail.save()
            else:
                current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
                html = render_to_string(
                    'product_module/include/product_incart.html',
                    {
                        'orders': current_order.orderdetails_set.filter(
                            product=product
                        ),
                        'product': product,
                    },
                    request=request
                )
                return JsonResponse({
                    'message': 'محصول موجود نیست',
                    'error': True,
                    'html': html
                })

    elif type == 'decrease':
        if product.is_byWeight:
            pack = order_detail.pack_size.size
            if order_detail.count == 1:
                order_detail.delete()
                product.q_back(1 , pack)
            else:
                order_detail.count -= 1
                order_detail.save()
                product.q_back(1 , pack)
        else:
            if order_detail.count == 1:
                order_detail.delete()
                product.q_back(1 , 1)
            else:
                order_detail.count -= 1
                order_detail.save()
                product.q_back(1 , 1)
    else:
        return JsonResponse({
            'message': 'درخواست نامعتبر',
            'error': True
        })

    current_order ,created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False ,user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'orders': current_order,
        'total': total_amount,
    }

    html = render_to_string(
        'product_module/include/product_incart.html',
        {
            'orders': current_order.orderdetails_set.filter(
                product=product
            ),
            'product': product,
        },
        request=request
    )


    return JsonResponse({
        'html': html,
        'error': False,
        'rem': product.quantity
    })






def change_order_count_basket(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    type = str(request.GET.get('type'))
    total_amount = 0
    total_items = 0
    total_weight = float(0)

    if detail_id is None or type is None:
        return JsonResponse({
            'message': 'خطای ناشناخته',
            'error': True
        })
    order_detail = OrderDetail.objects.filter(id=detail_id ,order__is_paid=False ,order__user=request.user).first()
    if order_detail is None:
        return JsonResponse({
            'message': 'جزئیات پیدا نشد',
            'error': True
        })

    product = order_detail.product

    if type == 'increase':
        if product.is_byWeight:
            pack = order_detail.pack_size.size
            if product.can_shop(1 , pack):
                product.shop(1 , pack)
                order_detail.count += 1
                order_detail.save()
            else:
                current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
                for order_detail in current_order.orderdetails_set.all():
                    total_amount += order_detail.total_price
                    total_items += order_detail.count
                total_weight = current_order.order_weight()
                html = render_to_string(
                    'order_module/basket_partial.html',
                    {
                        'orders': current_order,
                        'total_amount': total_amount,
                        'total_items': total_items,
                        'total_weight': total_weight
                    },
                    request=request
                )

                return JsonResponse({
                    'message': 'محصول موجود نیست',
                    'error': True,
                    'html': html
                })
        else:
            if product.can_shop(1 , 1):
                product.shop(1 , 1)
                order_detail.count += 1
                order_detail.save()
            else:
                current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
                for order_detail in current_order.orderdetails_set.all():
                    total_amount += order_detail.total_price
                    total_items += order_detail.count
                total_weight = current_order.order_weight()
                html = render_to_string(
                    'order_module/basket_partial.html',
                    {
                        'orders': current_order,
                        'total_amount': total_amount,
                        'total_items': total_items,
                        'total_weight': total_weight
                    },
                    request=request
                )

                return JsonResponse({
                    'message': 'محصول موجود نیست',
                    'error': True,
                    'html': html
                })

    elif type == 'decrease':
        if product.is_byWeight:
            pack = order_detail.pack_size.size
            if order_detail.count == 1:
                order_detail.delete()
                product.q_back(1 , pack)
            else:
                order_detail.count -= 1
                order_detail.save()
                product.q_back(1 , pack)
        else:
            if order_detail.count == 1:
                order_detail.delete()
                product.q_back(1 , 1)
            else:
                order_detail.count -= 1
                order_detail.save()
                product.q_back(1 , 1)
    else:
        return JsonResponse({
            'message': 'درخواست نامعتبر',
            'error': True
        })

    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False, user_id=request.user.id)
    for order_detail in current_order.orderdetails_set.all():
        total_amount += order_detail.total_price
        total_items += order_detail.count
    total_weight = current_order.order_weight()
    html = render_to_string(
        'order_module/basket_partial.html',
        {
            'orders': current_order,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_weight': total_weight
        },
        request=request
    )


    return JsonResponse({
        'html': html,
        'error': False,
        'rem': product.quantity
    })



def my_basket(request: HttpRequest):
    if request.user.is_authenticated:
        current_order ,create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid = False ,user_id=request.user.id)
        total_amount = current_order.calculate_total_price()
        total_items = current_order.total_items()
        total_weight = current_order.order_weight()
        related_products = Product.objects.filter(is_active=True ,quantity__gt=0).order_by('-created_at')
    else:
        return redirect('login_page')

    context = {
        'slider_title': 'جدیدترین محصولات',
        'related_products': related_products,
        'orders': current_order,
        'total_items': total_items,
        'total_amount': total_amount,
        'total_weight': total_weight,
    }
    return render(request ,'order_module/shopping_basket.html' ,context)

def delete_cart(request):
    current_order = Order.objects.filter(user=request.user ,is_paid=False).first()
    if current_order:
        order_detail = OrderDetail.objects.filter(order=current_order)
        for detail in order_detail:
            if detail.product.is_byWeight:
                detail.product.quantity += detail.count * detail.pack_size.size
                detail.product.save()
            else:
                detail.product.quantity += detail.count
                detail.product.save()
        current_order.delete()
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
        user = request.user
        provinces = Province.objects.all()
        cities = City.objects.all()
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        if not current_order.orderdetails_set.all():
            return redirect('my_basket_page')
        my_address = Address.objects.filter(user=request.user)
        total_amount = current_order.calculate_total_price()
        total_items = current_order.total_items()
        posting_methods = PostingMethod.objects.filter(is_active=True).order_by('order_type')

        msg = request.session.get('message')
        if msg:
            message = msg
            del request.session['message']

        context = {
            'orders': current_order,
            'my_address': my_address,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_weight': current_order.order_weight(),
            'address_form': address_form,
            'order_form': order_form,
            'message': message,
            'message_e': message_e,
            'popup_open': popup_open,
            'provinces': provinces,
            'cities': cities,
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
        cities = City.objects.all()
        current_order, create = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,user_id=request.user.id)
        my_address = Address.objects.filter(user=request.user)
        total_amount = current_order.calculate_total_price()
        total_items = current_order.total_items()
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
                    order = Order.objects.filter(user=request.user ,is_paid=False).first()
                    order.address = address
                    order.desc = desc
                    order.posting_method = posting
                    order.save()
                    return redirect('payment_page')
            else:
                message_e = 'در تکمیل سبد خرید مشکلی پیش آمده!'



        context = {
            'orders': current_order,
            'my_address': my_address,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_weight': current_order.order_weight(),
            'address_form': address_form,
            'order_form': order_form,
            'message': message,
            'message_e': message_e,
            'popup_open': popup_open,
            'provinces': provinces,
            'cities': cities,
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
        total_amount = current_order.include_postage_fee()
        total_items = current_order.total_items()
        total_weight = current_order.order_weight()
        postage_fee = current_order.postage_fee()
        payment_method = PaymentMethod.objects.all()

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
            pay_method = PaymentMethod.objects.get(id=pay)
            current_order.payment_method = pay_method
            current_order.save()
            if pay_method.id == 1:
                return redirect('deposit_page')
            else:
                return request_online_payment(request)

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
        payment_method = PaymentMethod.objects.get(id=1)
        current_order = Order.objects.filter(user=request.user ,is_paid=False ,payment_method=payment_method).first()
        if not current_order:
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
        payment_method = PaymentMethod.objects.get(id=1)
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
    online_pay_merchant = PaymentMethod.objects.filter(id=2).first()
    try:
        current_order ,created = Order.objects.get_or_create(is_paid=False ,is_done=False ,user=request.user)
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
        response = requests.post(settings.ZP_API_REQUEST ,data=json.dumps(req_data), headers=req_header)
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
            current_order = Order.objects.get(user=request.user ,is_paid=False)
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
                context = {
                    'error': 'پرداخت ناموفق!',
                    'returning': 'در حال انتقال به سبد خرید',
                    'redirect_url': reverse('my_basket_page'),
                }
                return render(request ,'order_module/include/payment_verify.html' ,context)

        else:
            context = {
                'error': 'پرداخت ناموفق!',
                'returning': 'در حال انتقال به سبد خرید',
                'redirect_url': reverse('my_basket_page'),
            }
            return render(request, 'order_module/include/payment_verify.html', context)
    else:
        context = {
            'error': 'پرداخت ناموفق!',
            'returning': 'در حال انتقال به سبد خرید',
            'redirect_url': reverse('my_basket_page'),
        }
        return render(request, 'order_module/include/payment_verify.html', context)


