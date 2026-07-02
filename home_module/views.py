from django.shortcuts import render
from pyexpat.errors import messages


# Create your views here.
def home(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request ,'home.html' ,context)