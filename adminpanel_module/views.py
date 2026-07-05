from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from utils.dashboard_decorators import get_sales_week, get_sales_week_growth, today, get_order_today, get_user_growth
from utils.my_decorators import permision_checker_decorator_factory


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
        'all_users': users['all_users'],
        'new_users': users['new_users'],
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
    date = today
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_user_card.html', {
        'user': user,
        'date': date
    })


def admin_popup_user_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_popup.html', {
        'user': user
    })