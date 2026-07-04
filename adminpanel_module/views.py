from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from utils.dashboard_decorators import get_sales_week
from utils.my_decorators import permision_checker_decorator_factory


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def index(request: HttpRequest):
    weeksale = get_sales_week()
    context = {
        'weeksales': weeksale['max_sale'],
        'weekdayssales': weeksale['days'],
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

def admin_popup_user_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_popup.html', {
        'user': user
    })