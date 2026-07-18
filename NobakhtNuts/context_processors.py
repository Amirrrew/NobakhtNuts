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
    if request.user.is_authenticated:
        basket = Order.objects.prefetch_related('orderdetails_set').filter(user=request.user ,is_paid=False).first()
        new_notifs = Notification.objects.filter(user=request.user ,is_seen=False).exists()
    brand = ProductBrand.objects.filter(is_active=True)
    columns = {}
    for i in range(1, 6):
        columns[i] = ProductCategory.objects.filter(column=i ,is_active=True)
    footers = FooterLinkBox.objects.prefetch_related('links').all()
    support_ways = SupportWays.objects.all()
    special_event = SpecialEvents.objects.filter(is_active=True).first()
    slider = SliderSlide.objects.filter(is_active=True).order_by('-is_primary')
    context = {
        'category': category,
        'brand': brand,
        'columns': columns,
        'basket': basket,
        'new_notifs': new_notifs,
        'footers': footers,
        'support_ways': support_ways,
        'special_event': special_event,
        'slider': slider
    }
    return context


