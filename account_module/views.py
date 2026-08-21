from datetime import timezone, timedelta, datetime
from time import sleep

from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from urllib.parse import urlencode
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from pyexpat.errors import messages
from random import SystemRandom

from polls.templatetags.poll_extras import register
from utils.my_decorators import send_sms, check_phone_blacklisted
from .models import User
from account_module.form import LoginForm, VerifySignupForm
from django.utils import timezone





class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        if request.user.is_authenticated:
            return redirect('edit_info_page')
        phone = None
        message_e = None
        if 'message_e' in request.session:
            message_e = request.session.get('message_e')
        if 'phone' in request.session:
            phone = request.session.get('phone')
            request.session.pop('phone')
        context = {'login_form': login_form ,'message_e': message_e ,'phone': phone}
        return render(request ,'account_module/login_form.html' , context)

    def post(self, request):
        message = None
        message_e = None
        login_form = LoginForm(request.POST)
        try:
            if login_form.is_valid():
                phone = login_form.cleaned_data.get('phone')
                is_blacklisted = check_phone_blacklisted(phone)
                if not is_blacklisted:
                    verify_sms = send_sms(phone)
                    if verify_sms.get('status') == 'عملیات موفق':
                        request.session['phone'] = phone
                        request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
                        request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
                        request.session['verify_code'] = verify_sms.get('code')
                        next_url = request.GET.get('next', '')
                        query = urlencode({
                            'next': next_url
                        })
                        return redirect(f"{reverse('verify_page')}?{query}")
                    else:
                        message_e = 'شماره تلفن اشتباه است!'
                else:
                    message_e = 'شماره تلفن اشتباه است!'
            else:
                message_e = "شماره تلفن خود را به درستی وارد کنید!"
        except Exception as e:
            message_e = f"در ورود مشکلی پیش آمده!"

        context = {'login_form': login_form , 'message_e': message_e , 'message': message}
        return render(request ,'account_module/login_form.html' , context)

class VerifyView(View):
    def get(self, request):
        verifysignup_form = VerifySignupForm()
        phone = request.session.get('phone')
        if not phone:
            return redirect('login_page')
        expire_time_front = request.session.get('verify_expiry_front')
        context = {'verifysignup_form': verifysignup_form ,'expire_time': expire_time_front}
        return render(request, 'account_module/verify_form.html', context)

    def post(self ,request):
        verifysignup_form = VerifySignupForm(request.POST)
        expire_time_front = request.session.get('verify_expiry_front')
        message_e = None
        try:
            if verifysignup_form.is_valid():
                verify_expiry = request.session.get('verify_expiry')
                verify_code_form = verifysignup_form.cleaned_data.get('verify_code')
                verify_code = request.session.get('verify_code')

                if not verify_expiry:
                    message_e = 'فرم نامعتبر!'
                else:
                    expire_time = datetime.fromisoformat(verify_expiry)
                    if timezone.now() > expire_time:
                        message_e = 'کد تایید منقضی شده!'
                    elif not verify_code_form == verify_code:
                        message_e = 'کد تایید اشتباه است!'
                    else:
                        phone = request.session.get('phone')
                        user = User.objects.filter(phone__iexact=phone).exists()

                        if not user:
                            new_user = User(
                                phone=phone,
                                is_active=True,
                                username=f'user-{get_random_string(10)}',
                            )
                            new_user.save()
                            login(request, new_user)
                        else:
                            user = User.objects.filter(phone__iexact=phone).first()
                            login(request ,user)


                        for key in ['verify_code' ,'verify_expiry','verify_expiry_front' ,'phone']:
                            request.session.pop(key,None)

                        next_url = request.GET.get('next')

                        if next_url:
                            return redirect(next_url)

                        return redirect('home')

        except Exception as e:
            message_e = f"در فعالسازی حساب مشکلی پیش آمده\n{str(e)}"

        context = {'verifysignup_form': verifysignup_form ,'message_e': message_e ,'expire_time': expire_time_front}
        return render(request, 'account_module/verify_form.html', context)

class ResetVerifyCode(View):
    def get(self, request):
        try:
            phone = request.session.get('phone')
            if phone:
                verify_sms = send_sms(phone)
                if verify_sms.get('status'):
                    request.session['phone'] = phone
                    request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
                    request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
                    request.session['verify_code'] = verify_sms.get('code')
                    return redirect(reverse('verify_page'))
                else:
                    request.session['message_e'] = 'در دریافت کد تایید مشکلی پیش آمد! دوباره امتحان کنید'
                    return redirect('register_page')
        except Exception as e:
            raise Http404


def reset_verify_phone(request):
    try:
        for key in ['verify_code', 'verify_expiry', 'verify_expiry_front']:
            request.session.pop(key, None)
            return redirect('login_page')
    except:
        return redirect('home')

# class LoginView(View):
#     def get(self, request):
#         login_form = LoginForm()
#         if request.user.is_authenticated:
#             return redirect(reverse('edit_info_page'))
#         if 'message' in request.session:
#             message = request.session.get('message')
#             del request.session['message']
#         else:
#             message = None
#         context = {'login_form': login_form ,'message': message}
#         return render(request ,'account_module/login_form.html' , context)
#
#     def post(self, request):
#         login_form = LoginForm(request.POST)
#         try:
#             if login_form.is_valid():
#                 phone = login_form.cleaned_data.get('phone')
#                 password = login_form.cleaned_data.get('password')
#                 user: User = User.objects.filter(phone__iexact=phone).first()
#                 if not user:
#                     message_e = 'کاربری با این شماره تلفن یافت نشد!'
#                 else:
#                     user_password = user.check_password(password)
#                     if user_password:
#                         if user.is_active:
#                             login(request, user)
#                             return redirect(reverse('home'))
#                         else:
#                             verify_sms = send_sms(phone)
#                             if verify_sms.get('status') == 'عملیات موفق':
#                                 request.session['phone'] = phone
#                                 request.session['password'] = password
#                                 request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
#                                 request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
#                                 request.session['verify_code'] = verify_sms.get('code')
#                                 request.session['form_type'] = 'login'
#                                 return redirect(reverse('verify_page'))
#                     else:
#                         message_e = 'رمز عبور اشتباه است!'
#             else:
#                 message_e = 'لطفا همه ی فیلد هارا پر کنید'
#         except Exception as e:
#             message_e = f'در ورود به حساب مشکلی پیش آمد\n{str(e)}'
#         context = {
#             'login_form': login_form,
#             'message_e': message_e,
#         }
#         return render(request ,'account_module/login_form.html' , context)


# class GetForgotUser(View):
#     def get(self, request):
#         get_form = GetForgotUserForm()
#         context = {'get_form': get_form}
#         return render(request ,'account_module/forgot_password.html' ,context)
#
#     def post(self, request):
#         get_form = GetForgotUserForm(request.POST)
#         try:
#             if get_form.is_valid():
#                 phone = get_form.cleaned_data.get('phone')
#                 user = User.objects.filter(phone__iexact=phone).first()
#                 message_e = None
#
#                 if user:
#                     verify_sms = send_sms(phone)
#                     if verify_sms.get('status') == 'عملیات موفق':
#                         request.session['phone'] = user.phone
#                         request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
#                         request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
#                         request.session['verify_code'] = verify_sms.get('code')
#                         request.session['form_type'] = 'reset_pass'
#                         return redirect(reverse('verify_page'))
#                     else:
#                         message_e = 'در ارسال کد تایید مشکلی پیش آمده!'
#                 else:
#                     message_e = "کاربری با این شماره تلفن وجود ندارد"
#         except:
#             message_e = 'خطای غیر منتظره'
#
#         context = {
#             'get_form': get_form,
#             'message_e': message_e,
#         }
#         return render(request ,'account_module/forgot_password.html' ,context)
#
#
#
# class ResetPassword(View):
#     def get(self, request):
#         reset_form = ResetPasswordForm()
#         context = {'reset_form': reset_form}
#         return render(request ,'account_module/reset_password_form.html' ,context)
#
#     def post(self, request):
#         reset_form = ResetPasswordForm(request.POST)
#         message_e = None
#         message = None
#
#         try:
#             if reset_form.is_valid():
#                 password = reset_form.cleaned_data.get('password')
#                 confirm_password = reset_form.cleaned_data.get('confirm_password')
#                 user = User.objects.filter(phone__iexact=request.session.get('phone')).first()
#                 if user:
#                     if password == confirm_password:
#                         user.set_password(password)
#                         user.save()
#                         request.session.pop('phone' ,None)
#                         request.session['message'] = 'رمز با موفقیت تغییر کرد! وارد حساب خود شوید'
#                         return redirect(reverse('login_page'))
#                     else:
#                         message_e = "پسورد ها با هم مطابقت ندارند!"
#                 else:
#                     message_e = "کاربر یافت نشد"
#         except Exception as e:
#             message_e = f'خطای غیرمنتظره\n{str(e)}'
#
#         context = {
#             'reset_form': reset_form,
#             'message_e': message_e,
#         }
#         return render(request ,'account_module/reset_password_form.html' ,context)

class Logout(View):
    def get(self, request):
        try:
            logout(request)
            return redirect(reverse('login_page'))
        except: return redirect('home')