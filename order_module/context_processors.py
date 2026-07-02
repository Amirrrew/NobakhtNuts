from order_module.models import Order, OrderDetail


def orders(request):
    context = {}
    if request.user.is_authenticated:
        orders = OrderDetail.objects.filter(order__user=request.user ,order__is_paid=False).select_related('product' ,'pack_size')
        context = {'orders': orders}
    return context
