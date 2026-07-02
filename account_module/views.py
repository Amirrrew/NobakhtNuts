from datetime import timezone, timedelta, datetime
from time import sleep

from PIL.ImagePalette import random
from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from pyexpat.errors import messages
from random import SystemRandom

from polls.templatetags.poll_extras import register
from utils.my_decorators import send_sms
from .models import User
from account_module.form import RegisterForm, LoginForm, VerifySignupForm, GetForgotUserForm, EnterForgotUserForm, \
    ResetPasswordForm
from django.utils import timezone


# Create your views here.



class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        message_e = None
        if 'message_e' in request.session:
            message_e = request.session.get('message_e')
        context = {'register_form': register_form ,'message_e': message_e}
        return render(request ,'account_module/register_form.html' , context)

    def post(self, request):
        message = None
        message_e = None
        register_form = RegisterForm(request.POST)
        try:
            if register_form.is_valid():
                phone = register_form.cleaned_data.get('phone')
                password = register_form.cleaned_data.get('password')
                user = User.objects.filter(phone__iexact=phone).exists()

                if user:
                    message_e = 'یک حساب با این شماره تلفن وجود دارد!'
                else:
                    verify_sms = send_sms(phone)
                    sleep(1)
                    if verify_sms.get('status') == 'عملیات موفق':
                        request.session['phone'] = phone
                        request.session['password'] = password
                        request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
                        request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
                        request.session['verify_code'] = verify_sms.get('code')
                        request.session['form_type'] = 'register'
                        return redirect(reverse('verify_page'))
                    else:
                        message_e = 'شماره تلفن اشتباه است!'
            else:
                message_e = "لطفا همه ی فیلد هارا پر کنید"
        except:
            message_e = f" در ثبت نام مشکلی پیش آمد!"

        context = {'register_form': register_form , 'message_e': message_e , 'message': message}
        return render(request ,'account_module/register_form.html' , context)

class VerifyView(View):
    def get(self, request):
        verifysignup_form = VerifySignupForm()
        phone = request.session.get('phone')
        password = request.session.get('password')
        if not password and not phone:
            return redirect('register_form')
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
                form_type = request.session.get('form_type')

                if not verify_expiry:
                    message_e = 'کد تایید منقضی شده!'
                else:
                    expire_time = datetime.fromisoformat(verify_expiry)
                    if timezone.now() > expire_time:
                        message_e = 'کد تایید منقضی شده!'
                    elif not verify_code_form == verify_code:
                        message_e = 'کد تایید اشتباه است!'
                    else:
                        phone = request.session.get('phone')
                        password = request.session.get('password')

                        if form_type == 'register':
                            user = User.objects.filter(phone__iexact=phone).exists()
                            if not user:
                                new_user = User(
                                    phone=phone,
                                    is_active=True,
                                    username=f'user-{get_random_string(10)}',
                                )
                                new_user.set_password(password)
                                new_user.save()
                                login(request, new_user)
                            else:
                                login(request ,User.objects.filter(phone__iexact=phone).first())

                        elif form_type == 'login':
                            user = User.objects.filter(phone__iexact=phone).first()
                            login(request, user)

                        elif form_type == 'reset_pass':
                            request.session['forgot_phone'] = phone
                            return redirect('reset_password_page')

                        for key in ['verify_code' ,'verify_expiry','verify_expiry_front' ,'phone' ,'password']:
                            request.session.pop(key,None)

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




class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        if request.user.is_authenticated:
            return redirect(reverse('edit_info_page'))
        if 'message' in request.session:
            message = request.session.get('message')
            del request.session['message']
        else:
            message = None
        context = {'login_form': login_form ,'message': message}
        return render(request ,'account_module/login_form.html' , context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        try:
            if login_form.is_valid():
                phone = login_form.cleaned_data.get('phone')
                password = login_form.cleaned_data.get('password')
                user: User = User.objects.filter(phone__iexact=phone).first()
                if not user:
                    message_e = 'کاربری با این شماره تلفن یافت نشد!'
                else:
                    user_password = user.check_password(password)
                    if user_password:
                        if user.is_active:
                            login(request, user)
                            return redirect(reverse('home'))
                        else:
                            verify_sms = send_sms(phone)
                            if verify_sms.get('status') == 'عملیات موفق':
                                request.session['phone'] = phone
                                request.session['password'] = password
                                request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
                                request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
                                request.session['verify_code'] = verify_sms.get('code')
                                request.session['form_type'] = 'login'
                                return redirect(reverse('verify_page'))
                    else:
                        message_e = 'رمز عبور اشتباه است!'
            else:
                message_e = 'لطفا همه ی فیلد هارا پر کنید'
        except Exception as e:
            message_e = f'در ورود به حساب مشکلی پیش آمد\n{str(e)}'
        context = {
            'login_form': login_form,
            'message_e': message_e,
        }
        return render(request ,'account_module/login_form.html' , context)


class GetForgotUser(View):
    def get(self, request):
        get_form = GetForgotUserForm()
        context = {'get_form': get_form}
        return render(request ,'account_module/forgot_password.html' ,context)

    def post(self, request):
        get_form = GetForgotUserForm(request.POST)
        try:
            if get_form.is_valid():
                phone = get_form.cleaned_data.get('phone')
                user = User.objects.filter(phone__iexact=phone).first()
                message_e = None

                if user:
                    verify_sms = send_sms(phone)
                    if verify_sms.get('status') == 'عملیات موفق':
                        request.session['phone'] = user.phone
                        request.session['verify_expiry'] = (timezone.now() + timedelta(seconds=120)).isoformat()
                        request.session['verify_expiry_front'] = (timezone.now() + timedelta(seconds=120)).timestamp()
                        request.session['verify_code'] = verify_sms.get('code')
                        request.session['form_type'] = 'reset_pass'
                        return redirect(reverse('verify_page'))
                    else:
                        message_e = 'در ارسال کد تایید مشکلی پیش آمده!'
                else:
                    message_e = "کاربری با این شماره تلفن وجود ندارد"
        except:
            message_e = 'خطای غیر منتظره'

        context = {
            'get_form': get_form,
            'message_e': message_e,
        }
        return render(request ,'account_module/forgot_password.html' ,context)



class ResetPassword(View):
    def get(self, request):
        reset_form = ResetPasswordForm()
        context = {'reset_form': reset_form}
        return render(request ,'account_module/reset_password_form.html' ,context)

    def post(self, request):
        reset_form = ResetPasswordForm(request.POST)
        message_e = None
        message = None

        try:
            if reset_form.is_valid():
                password = reset_form.cleaned_data.get('password')
                confirm_password = reset_form.cleaned_data.get('confirm_password')
                user = User.objects.filter(phone__iexact=request.session.get('phone')).first()
                if user:
                    if password == confirm_password:
                        user.set_password(password)
                        user.save()
                        request.session.pop('phone' ,None)
                        request.session['message'] = 'رمز با موفقیت تغییر کرد! وارد حساب خود شوید'
                        return redirect(reverse('login_page'))
                    else:
                        message_e = "پسورد ها با هم مطابقت ندارند!"
                else:
                    message_e = "کاربر یافت نشد"
        except Exception as e:
            message_e = f'خطای غیرمنتظره\n{str(e)}'

        context = {
            'reset_form': reset_form,
            'message_e': message_e,
        }
        return render(request ,'account_module/reset_password_form.html' ,context)

class Logout(View):
    def get(self, request):
        try:
            logout(request)
            request.session['message'] = 'از حساب با موفقیت خارج شدید'
            return redirect(reverse('login_page'))
        except: request.session['message'] = 'خروج از حساب با مشکل مواجه شد'