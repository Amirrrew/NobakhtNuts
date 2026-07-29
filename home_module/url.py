from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.home , name='home'),
    path('offline/' ,views.YoureOffline.as_view())
]