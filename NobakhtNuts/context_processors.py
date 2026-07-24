from django.http import JsonResponse
from unicodedata import category

from account_module.models import Notification
from home_module.models import SpecialEvents, SliderSlide
from order_module.models import OrderDetail, Order
from product_module.models import ProductCategory, ProductSubCategory, ProductBrand, Product
from site_settings.models import FooterLinkBox
from support_module.models import SupportWays


def global_context(request):
    category = ProductCategory.objects.filter(is_active=True).prefetch_related('subcategory')
    basket =None
    new_notifs = None
    ongoing_order = None
    if request.user.is_authenticated:
        basket = Order.objects.prefetch_related('orderdetails_set').filter(user=request.user ,is_paid=False).first()
        new_notifs = Notification.objects.filter(user=request.user ,is_seen=False).exists()
        ongoing_order = Order.objects.filter(user=request.user, is_paid=True, is_done=False).exists()
    footers = FooterLinkBox.objects.prefetch_related('links').all()
    support_ways = SupportWays.objects.all()
    context = {
        'category': category,
        'basket': basket,
        'new_notifs': new_notifs,
        'footers': footers,
        'support_ways': support_ways,
        'ongoing_order': ongoing_order,
    }
    return context


