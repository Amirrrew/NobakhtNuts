from django.shortcuts import render
from pyexpat.errors import messages

from home_module.models import SpecialEvents, SliderSlide, Carousel, CarouselItem, CardBlock
from product_module.models import Product


# Create your views here.
def home(request):
    user = request.user
    special_event = SpecialEvents.objects.filter(is_active=True).first()
    slider = SliderSlide.objects.filter(is_active=True).order_by('-is_primary')
    special_carousel = Carousel.objects.prefetch_related("carousel_set__product").filter(
        is_active=True
    ).first()
    carousel_exist = bool(special_carousel)
    card_block = CardBlock.objects.prefetch_related('cardblock_set').filter(is_active=True).first()


    context = {
        'user': user,
        'special_event': special_event,
        'slider': slider,
        'is_carousel': carousel_exist,
        'special_carousel': special_carousel or Product.objects.filter(is_active=True ,is_deleted=False ,offer__gt=0).order_by('-chosen' ,'-created_at')[:10],
        'card_block': card_block,
    }
    return render(request, 'home_module/home.html', context)