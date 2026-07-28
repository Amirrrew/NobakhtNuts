from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.template.context_processors import request
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView
from iranian_cities.models import Province ,City
import slugify


from account_module.models import User, Address, Notification
from django.shortcuts import render, redirect, get_object_or_404

from order_module.context_processors import orders
from order_module.models import OrderStatus, Order
from support_module.form import NewTicketForm
from support_module.models import Ticket, TicketReason, TicketStatus
from userpanel_module.form import EditInfoForm, ResetPasswordFormPanel, NewAddressForm


@login_required
def side_bar(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    context = {
        'user': user,
    }
    return render(request ,'userpanel_module/components/side_bar.html', context)

@login_required
def index(request: HttpRequest):
    # user = User.objects.filter(id=request.user.id).first()
    # ongoing_order = Order.objects.filter(user=user ,is_paid=True ,is_done=False).first()
    # ongoing_tickets = Ticket.objects.filter(user=user)

    return redirect('edit_info_page')

    # context = {
    #     'user': user,
    #     'orders': ongoing_order,
    #     'tickets': ongoing_tickets,
    # }
    # return render(request ,'userpanel_module/panel_index.html' ,context)


@method_decorator(login_required , name='dispatch')
class EditInfo(View):
    def get(self,request: HttpRequest):
        user = User.objects.filter(id=request.user.id).first()
        edit_form = EditInfoForm()
        context = {
            'edit_form': edit_form,
            'user': user,
        }
        return render(request ,'userpanel_module/edit_info.html' ,context)

    def post(self,request: HttpRequest):
        user = User.objects.filter(id=request.user.id).first()
        edit_form = EditInfoForm(request.POST, request.FILES ,instance=user)
        username = request.POST['username']
        username_exist = User.objects.filter(username=username).exists()
        avatar = request.FILES.get('avatar')
        message = None
        message_e = None

        try:
            if edit_form.is_valid():
                if avatar:
                    user.avatar = avatar
                edit_form.save(commit=True)
                message = "تغییرات با موفقیت ذخیره شد"
            else:
                message_e = "این نام کاربری قبلا استفاده شده! یکی دیگر امتحان کنید"
        except:
            message_e = 'در ذخیره اطلاعات مشکلی پیش آمد'

        context = {
            'edit_form': edit_form,
            'user': user,
            'message': message,
            'message_e': message_e,
        }
        return render(request ,'userpanel_module/edit_info.html' ,context)




@method_decorator(login_required , name='dispatch')
class ResetPassword(View):
    def get(self,request: HttpRequest):
        reset_form = ResetPasswordFormPanel()
        context = {
            'reset_form': reset_form,
        }
        return render(request ,'userpanel_module/reset_password.html' ,context)

    def post(self,request: HttpRequest):
        user = User.objects.filter(username=request.user.username).first()
        reset_form = ResetPasswordFormPanel(request.POST)
        message = None
        message_e = None

        if reset_form.is_valid():
            reset_form.save(commit=False)
            user.set_password(reset_form.cleaned_data['password'])
            user.save()
            request.session['message'] = 'رمز عبور با موفقیت تغییر کرد'
            return redirect(reverse('login_page'))
        else:
            message_e = 'رمز های عبور با هم مطابقت ندارند'

        context = {
            'reset_form': reset_form,
            'message_e': message_e,
        }
        return render(request ,'userpanel_module/reset_password.html' ,context)

@method_decorator(login_required , name='dispatch')
class DeleteAvatar(View):
    def get(self,request: HttpRequest):
        user = User.objects.filter(username=request.user.username).first()
        if user:
            user.avatar = None
            user.save()
            return redirect(reverse('edit_info_page'))


@method_decorator(login_required , name='dispatch')
class MyAddress(View):
    def get(self ,request: HttpRequest):
        address_form = NewAddressForm()
        user = request.user
        message = None
        address = Address.objects.filter(user=user)
        provinces = Province.objects.all()
        cities = City.objects.all()
        msg = request.session.get('message')
        if msg:
            message = msg
            del request.session['message']
        context = {
            'address': address,
            'provinces': provinces,
            'cities': cities,
            'user': user,
            'address_form': address_form,
            'message': message,
        }
        return render(request ,'userpanel_module/my_address.html' ,context)

    def post(self,request:HttpRequest):
        address_form = NewAddressForm(request.POST)
        user = request.user
        provinces = Province.objects.all()
        cities = City.objects.all()
        address = Address.objects.filter(user=user)
        message = None
        message_e = None
        popup_open = None
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
                user = user,
                receiver=receiver,
                is_Default= False,
            )

            new_address.save()
            request.session['message'] = 'آدرس جدید با موفقیت ثبت شد'
            return redirect('my_address_page')
        else:
            message_e = "لطفا همه فیلد هارا به درستی پر کنید"
            popup_open = True

        context = {
            'address': address,
            'provinces': provinces,
            'cities': cities,
            'user': user,
            'address_form': address_form,
            'message': message,
            'message_e': message_e,
            'popup_open': popup_open,
        }
        return render(request ,'userpanel_module/my_address.html' ,context)


@login_required
def DeleteAddress(request: HttpRequest ,pk):
    address = get_object_or_404(Address ,pk=pk ,user=request.user)
    address.delete()
    return redirect(reverse('my_address_page'))

def get_cities(request):
    province_id = request.GET.get("province_id")
    cities = City.objects.filter(
        province_id=province_id
    ).values("id", "name")

    return JsonResponse(list(cities), safe=False)

@method_decorator(login_required , name='dispatch')
class MyTickets(View):
    def get(self ,request: HttpRequest):
        template_name = 'userpanel_module/my_tickets.html'
        ticket_form = NewTicketForm()
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        ticket_reasons = TicketReason.objects.all()
        context = {
            'ticket_form': ticket_form,
            'tickets': tickets,
            'ticket_reasons': ticket_reasons,
        }
        return render(request ,template_name ,context)

    def post(self ,request: HttpRequest):
        template_name = 'userpanel_module/my_tickets.html'
        ticket_form = NewTicketForm(request.POST ,request.FILES)
        ticket_reasons = TicketReason.objects.all()
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        message = None
        message_e = None
        popup_open = None
        try:
            if request.user.is_authenticated:
                if ticket_form.is_valid():
                    title = ticket_form.cleaned_data.get('title')
                    reason_selected = request.POST.get('reason')
                    text = ticket_form.cleaned_data.get('text')
                    image = request.FILES.get('image')



                    reason = TicketReason.objects.filter(id=reason_selected).first()
                    status = TicketStatus.objects.get(id=1)

                    if not title:
                        message_e = 'برای تیکت یک عنوان بنویسید'
                    if not text:
                        message_e = 'مشکل خود را شرح دهید'
                    else:
                        new_ticket = Ticket(
                            title=title,
                            reason=reason,
                            text=text,
                            status=status,
                            user=request.user,
                        )
                        if image:
                            new_ticket.img = image
                        new_ticket.save()
                        message = 'تیکت با موفقیت ارسال شد!'
                else:
                    message_e = 'تمام فیلد هارا به درستی پر کنید'
                    popup_open = True
            else:
                message_e = 'برای ارسال تیکت ابتدا باید وارد شوید'
        except:
            message_e = 'مشکلی در ارسال تیکت پیش آمده!'
            popup_open = True


        context = {
            'tickets': tickets,
            'ticket_form': ticket_form,
            'message': message,
            'message_e': message_e,
            'ticket_reasons': ticket_reasons,
            'popup_open': popup_open,
        }
        return render(request ,template_name ,context)

@method_decorator(login_required , name='dispatch')
class DeleteTicket(View):
    def get(self ,request: HttpRequest ,pk):
        ticket = get_object_or_404(Ticket, pk=pk ,user=request.user)
        if ticket:
            ticket.delete()
        return redirect(reverse('my_tickets_page'))


@method_decorator(login_required ,name='dispatch')
class My_orders(ListView):
    model = Order
    template_name = 'userpanel_module/my_orders_partial.html'

    def get_context_data(self ,*args,**kwargs):
        context = super(My_orders ,self).get_context_data(*args,**kwargs)
        return context

    def get_queryset(self):
        query = super(My_orders ,self).get_queryset()
        query = Order.objects.prefetch_related('orderdetails_set').filter(is_paid=True ,user=self.request.user).order_by('-payment_date')
        return query


@method_decorator(login_required ,name='dispatch')
class Order_details(DetailView):
    model = Order
    template_name = 'userpanel_module/include/order_details.html'

    def get_context_data(self ,*args,**kwargs):
        context = super(Order_details ,self).get_context_data(*args ,**kwargs)
        message = self.request.session.get('message')
        if message:
            context['message'] = 'سفارش با موفقیت ثبت شد!'
            del self.request.session['message']
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        except:
            return redirect('my_orders_page')


@method_decorator(login_required , name='dispatch')
class My_notifications(ListView):
    model = Notification
    template_name = 'userpanel_module/notifications.html'

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('is_read' ,'-created_at')

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login_page')

        Notification.objects.filter(
            user=request.user,
            is_seen=False
        ).update(is_seen=True)

        return super().get(request, *args, **kwargs)

@method_decorator(login_required , name='dispatch')
class Notif_detail(DetailView):
    model = Notification
    template_name = 'userpanel_module/include/notifications_detail.html'

    def get(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()

        return super().get(request, *args, **kwargs)


def delete_notif(request ,pk):
    try:
        notification = Notification.objects.filter(pk=pk).first()
        if notification:
            notification.delete()
        return redirect('notifications_page')
    except:
        return redirect('home')

def OrderFinish(request ,pk):
    order = Order.objects.filter(pk=pk).first()
    if order:
        order.status = OrderStatus.objects.filter(title='پایان یافته').first()
        order.is_done = True
        order.save()
    return redirect('order_detail_page' ,pk=pk)

def OrderCancel(request,pk):
    order = Order.objects.filter(pk=pk).first()
    if order:
        order.cancel_order()
    return redirect('order_detail_page' ,pk=pk)
