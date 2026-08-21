from django.db.models import Prefetch, Count ,Avg ,Q
from django.shortcuts import render
from pyexpat.errors import messages
from unicodedata import category

from article_module.models import Article
from home_module.models import SpecialEvents, LandingPage, Carousel, CarouselItem, CardBlock, Banner, HomeCards
from product_module.models import Product, ProductImage
from django.views.generic import View, TemplateView, ListView
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

def not_found(request ,exception):
    return render(request ,'include/404.html' ,status=404)

class Home(TemplateView):
    template_name = 'home_module/home.html'


    def get_context_data(self, *args, **kwargs):
        context = super(Home ,self).get_context_data(**kwargs)

        user = self.request.user
        special_event = SpecialEvents.objects.filter(is_active=True).first()
        special_carousel = (
            Carousel.objects
            .filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    'carousel_set',
                    queryset=CarouselItem.objects.select_related(
                        'product',
                        'product__category',
                        'product__brand',
                    ).prefetch_related(
                        'product__packs',
                        Prefetch(
                            'product__product_image',
                            queryset=ProductImage.objects.order_by('-is_Main', 'id'),
                            to_attr='prefetched_images'
                        )
                    )
                    .annotate(comments_total=Count('product__comment_set' ,distinct=True),rating_avarage=Avg('product__comment_set__rating'))
                )
            )
            .first()
        )
        carousel_exist = bool(special_carousel)
        card_block = CardBlock.objects.filter(is_active=True).prefetch_related(Prefetch('cardblock_set' ,queryset=HomeCards.objects.select_related('category').annotate(products_count=Count('category__products' ,filter=Q(category__products__is_active=True ,category__products__is_deleted=False))))).first()
        banners = Banner.objects.select_related('category', 'sub_category').filter(is_active=True)
        recent_articles = Article.objects.select_related('author').filter(is_active=True).order_by('-created_at')[:10]

        context['user'] = user
        context['special_event'] = special_event
        context['is_carousel'] = carousel_exist
        context['special_carousel'] = special_carousel or (Product.objects.filter(is_active=True,is_deleted=False,category__is_active=True ,offer__gt=0 ,quantity__gt=0).select_related('category','category__main_category' ,'brand').prefetch_related('packs' ,Prefetch('product_image' ,queryset=ProductImage.objects.order_by('-is_Main' ,'id'),to_attr='prefetched_images')).annotate(comments_total=Count('comment_set' ,distinct=True),rating_avarage=Avg('comment_set__rating')).order_by('-chosen' ,'-created_at'))
        context['card_block'] = card_block
        context['banners']= banners
        context['articles']= recent_articles
        return context