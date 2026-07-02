from django.urls import path
from . import views

urlpatterns = [
    path('register/' ,views.RegisterView.as_view(),name='register_page'),
    path('login/' ,views.LoginView.as_view(),name='login_page'),
    path('verify/' ,views.VerifyView.as_view(),name='verify_page'),
    path('reset-verify-code/' ,views.ResetVerifyCode.as_view(),name='reset_verify_code'),
    path('forgot-password/' ,views.GetForgotUser.as_view(),name='forgot_user_get_page'),
    path('reset-password/' ,views.ResetPassword.as_view(),name='reset_password_page'),
    path('logout/' ,views.Logout.as_view(),name='logout'),
]