from django.core.cache import cache
from django.http import JsonResponse
from unicodedata import category

from account_module.models import Notification
from home_module.models import SpecialEvents, LandingPage
from order_module.models import OrderDetail, Order
from product_module.models import ProductCategory, ProductSubCategory, ProductBrand, Product
from site_settings.models import FooterLinkBox
from support_module.models import SupportWays


def global_context(request):
    basket =None
    new_notifs = None
    navigation = cache.get('global_navigation')

    if navigation is None:
        navigation = {
            'category': ProductCategory.objects.filter(is_active=True).prefetch_related('subcategory'),
            'footers': FooterLinkBox.objects.prefetch_related('links').all(),
            'support_ways': SupportWays.objects.all(),
        }
        cache.set('global_navigation' ,navigation ,60*15)
    context = navigation.copy()

    if request.user.is_authenticated:
        context["basket"] = (
            Order.objects
            .filter(user=request.user, is_paid=False)
            .prefetch_related("orderdetails_set")
            .first()
        )
        context["new_notifs"] = Notification.objects.filter(
            user=request.user,
            is_seen=False,
        ).exists()

    return context


