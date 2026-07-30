from django.shortcuts import render
from pyexpat.errors import messages

from home_module.models import SpecialEvents, SliderSlide, Carousel, CarouselItem, CardBlock, Banner
from product_module.models import Product
from django.views.generic import View, TemplateView
from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404


class ServiceWorkerView(View):
    def get(self, request):
        path = finders.find("../static/scripts/service-worker.js")
        if not path:
            raise Http404()
        return FileResponse(
            open(path, "rb"),
            content_type="application/javascript",
        )

class YoureOffline(TemplateView):
    template_name = 'offline.html'

def home(request):
    user = request.user
    special_event = SpecialEvents.objects.filter(is_active=True).first()
    slider = SliderSlide.objects.filter(is_active=True).order_by('-is_primary')
    special_carousel = Carousel.objects.prefetch_related("carousel_set__product").filter(
        is_active=True
    ).first()
    carousel_exist = bool(special_carousel)
    card_block = CardBlock.objects.prefetch_related('cardblock_set').filter(is_active=True).first()
    banners = Banner.objects.select_related('category' ,'sub_category').filter(is_active=True)

    context = {
        'user': user,
        'special_event': special_event,
        'slider': slider,
        'is_carousel': carousel_exist,
        'special_carousel': special_carousel or Product.objects.filter(is_active=True ,is_deleted=False ,offer__gt=0).order_by('-chosen' ,'-created_at')[:10],
        'card_block': card_block,
        'banners': banners
    }
    return render(request, 'home_module/home.html', context)