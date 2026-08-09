from django.urls import path
from . import views

urlpatterns = [
    path('about-us/' ,views.About_us.as_view() ,name='about_us'),
    path('faq/' ,views.FAQ.as_view() ,name='faq'),
    path('policies' ,views.Policies.as_view() ,name='policies'),
    path('bulk-buy' ,views.BulkBuy.as_view() ,name='bulk_buy')
]