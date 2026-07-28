from django.urls import path
from . import views
from account_module.views import Logout

urlpatterns = [
    path('' ,views.index , name='user_panel'),
    path('edit-info/' ,views.EditInfo.as_view(),name='edit_info_page'),
    path('logout/' ,Logout.as_view(),name='logout_page'),
    path('my-address/' ,views.MyAddress.as_view(),name='my_address_page'),
    path('my-tickets/' ,views.MyTickets.as_view(),name='my_tickets_page'),
    path('delete-avatar/' ,views.DeleteAvatar.as_view(),name='delete_avatar_page'),
    path('my-address/<int:pk>/delete/' ,views.DeleteAddress,name='delete_address_page'),
    path('my-ticket/<int:pk>/delete/' ,views.DeleteTicket.as_view(),name='delete_ticket_page'),
    path('my-orders/' ,views.My_orders.as_view(),name='my_orders_page'),
    path('my-orders/details/<int:pk>' ,views.Order_details.as_view(),name='order_detail_page'),
    path('notifications/' ,views.My_notifications.as_view(),name='notifications_page'),
    path('notifications/<int:pk>/' ,views.Notif_detail.as_view(),name='notif_detail_page'),
    path('notifications/<int:pk>/delete/' ,views.delete_notif,name='notif_delete_page'),
    path("get-cities/", views.get_cities, name="get_cities"),
    path('order-finished/<int:pk>/' ,views.OrderFinish ,name='my_order_finished'),
    path('order-cancel/<int:pk>/', views.OrderCancel, name='my_order_cancel'),
]