from django.shortcuts import render

def index(request):
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