from itertools import count

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView

from order_module.context_processors import orders
from order_module.models import Order, OrderStatus
from utils.dashboard_decorators import get_sales_week, get_sales_week_growth, today, get_order_today, get_user_growth, \
    get_new_orders, get_lowstock_products, get_best_selling_products, get_new_tickets
from utils.my_decorators import permision_checker_decorator_factory
from django.db.models import Q


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def index(request: HttpRequest):
    weeksale = get_sales_week()
    weeksale_growth = get_sales_week_growth()
    users = get_user_growth()
    order_today = get_order_today()
    context = {
        'weeksales': weeksale['max_sale'],
        'weekdayssales': weeksale['days'],
        'total_week_sale': weeksale['total_week_sale'],
        'weeksale_growth': weeksale_growth['percent'],
        'order_count_today': order_today['today_orders'],
        'order_difference': order_today['difference_orders'],
        'today_total': order_today['today_total'],
        'yesterday_total': order_today['yesterday_total'],
        'total_order_growth': order_today['percent'],
        'new_orders': get_new_orders(),
        'all_users': users['all_users'],
        'new_users': users['new_users'],
        'low_stock_products': get_lowstock_products(),
        'best_selling_products': get_best_selling_products(),
        'new_tickets': get_new_tickets(),
    }
    return render(request, 'adminpanel_module/home/admin_home.html', context)

def admin_sidebar_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_sidebar_component.html', {
        'user': user
    })

def admin_header_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_header_component.html', {
        'user': user
    })

def admin_user_card_component(request):
    context = {
        'new_orders': get_new_orders(),
        'new_tickets': get_new_tickets(),
        'user': request.user,
        'date': today
    }
    return render(request, 'adminpanel_module/shared/components/admin_user_card.html', context)


def admin_popup_user_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_popup.html', {
        'user': user
    })

def admin_popup_notif_component(request):
    context = {
        'new_orders': get_new_orders(),
        'new_tickets': get_new_tickets(),
        'user': request.user,
    }
    return render(request, 'adminpanel_module/shared/components/admin_popup_notif_component.html', context)

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class OrdersListView(ListView):
    model = Order
    template_name = 'adminpanel_module/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('q')

        queryset = Order.objects.filter(
            is_paid=True
        ).order_by('is_done', '-payment_date' )

        if search:
            if search.isdigit():
                queryset = queryset.filter(
                    Q(pk__icontains=int(search)) |
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )

        return queryset

    def get(self ,request , *args , **kwargs):
        response = super().get(request, *args , **kwargs)
        if request.GET.get('q') is not None:
            html = render_to_string(
                'adminpanel_module/orders/table_components/order_table_partial.html',
                {'orders': self.object_list},
                request=request
            )

            return JsonResponse({
                'html': html,
                'data_length': self.object_list.count() if hasattr(self.object_list, 'count') else len(self.object_list)
            })

        return response

@login_required
def OrderDelete(request ,pk):
    order = get_object_or_404(Order, pk=pk)
    if order:
        order.delete()
    return redirect('admin_order_list')

@login_required
def OrderSelectedAction(request):
    action = request.GET.get('action')
    orders_ids = request.POST.getlist('order')
    message=None
    if action and orders_ids:
        orders_list = Order.objects.filter(id__in=orders_ids)
        if action == 'delete':
            orders_list.delete()
            message = 'سفارشات با موفقیت حذف شدند'
        elif action == 'approve':
            for order in orders_list:
                order.approve_order()
                message = 'سفارشات تایید شده و در مرحله آماده سازی قرار گرفتند'
        elif action == 'reject':
            for order in orders_list:
                order.reject_order()
                message = 'سفارشات با موفقیت رد شدند'
        elif action == 'send':
            for order in orders_list:
                order.send_order()
                message = 'سفارشات با موفقیت در مرحله ارسال شده قرار گرفتند'

    orders_after = Order.objects.filter(is_paid=True).order_by('is_done', '-payment_date' )
    html = render_to_string(
        'adminpanel_module/orders/table_components/order_table_partial.html',
        {'orders': orders_after},
        request=request
    )

    return JsonResponse({
        'html': html,
        'message': message
    })

class OrderDetailView(DeleteView):
    model = Order
    template_name = 'adminpanel_module/orders/order_details_admin.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object
        action = request.POST.get('order_action')
        if action == 'approve':
            order.approve_order()
        elif action == 'reject':
            order.reject_order()
        elif action == 'send':
            order.send_order()
        elif action == 'cancel':
            order.return_order()

        return redirect('admin_order_detail' ,pk=order.pk)

