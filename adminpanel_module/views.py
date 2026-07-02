from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from utils.my_decorators import permision_checker_decorator_factory


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def index(request: HttpRequest):
    return render(request ,'home/admin_home.html' ,{})

def admin_sidebar_component(request):
    user = request.user
    return render(request, 'shared/components/admin_sidebar_component.html' ,{
        'user': user
    })

def admin_header_component(request):
    user = request.user
    return render(request ,'shared/components/admin_header_component.html' ,{
        'user': user
    })

def admin_popup_user_component(request):
    user = request.user
    return render(request ,'shared/components/admin_popup.html' ,{
        'user': user
    })