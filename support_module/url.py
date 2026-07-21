from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.SupportView.as_view(), name='support_page'),
]