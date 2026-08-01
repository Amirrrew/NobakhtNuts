from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order/' , views.add_to_order, name='add_to_order'),
    path('change-order-count/' , views.change_order_count, name='change_order_count'),
    path('my-basket/' ,views.my_basket, name='my_basket_page'),
    path('checkout/' ,views.BasketCheckout.as_view(), name='checkout_page'),
    path('payment/', views.BasketPayment.as_view(), name='payment_page'),
    path('deposit/' ,views.Deposit.as_view(), name='deposit_page'),
    path('request-payment/', views.request_online_payment, name='request_online_payment'),
    path('verify-payment/' ,views.verify_payment, name='verify_payment'),
    path('delete-basket/' , views.delete_cart, name='delete_basket'),
    path('apply-fee/' ,views.get_postage_fee ,name='apply_postage_fee'),
    path('item-not-available' ,views.NaItemView.as_view() ,name='na_item'),
    path('apply-code/' ,views.apply_discount ,name='apply_code')
]