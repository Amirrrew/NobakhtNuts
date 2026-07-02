from django.contrib import admin

from order_module.models import OrderDetail, Order, OrderStatus, PaymentMethod, PostingMethod, Cards


# Register your models here.
class OrderDetailAdmin(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' ,'is_paid' ,'status' ,]
    list_filter = ['is_paid']
    inlines = [OrderDetailAdmin]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(PaymentMethod)
admin.site.register(PostingMethod)
admin.site.register(Cards)

