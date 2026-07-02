from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.SupportView.as_view(), name='support_page'),
    path('about-us/' ,views.AboutUsView.as_view(), name='about_us'),
]