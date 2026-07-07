from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index, name='admin_home'),
    path('orders/' ,views.OrdersListView.as_view() ,name='admin_order_list'),
    path('orders/delete/<int:pk>' ,views.OrderDelete ,name='admin_order_delete'),
    path('orders/action/' ,views.OrderSelectedAction ,name='admin_order_action'),
    path('orders/<int:pk>' ,views.OrderDetailView.as_view() ,name='admin_order_detail'),
]