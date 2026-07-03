from django.urls import path
from . import views

urlpatterns = [
    path('login/' ,views.LoginView.as_view(),name='login_page'),
    path('verify/' ,views.VerifyView.as_view(),name='verify_page'),
    path('reset-verify-code/' ,views.ResetVerifyCode.as_view(),name='reset_verify_code'),
    path('reset-verify-phone' ,views.reset_verify_phone ,name='reset_phone_number'),
    path('logout/' ,views.Logout.as_view(),name='logout'),
]