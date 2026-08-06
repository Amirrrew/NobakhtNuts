from gc import get_objects
from itertools import product

from django.contrib.messages.context_processors import messages
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.template.defaultfilters import title
from django.template.defaulttags import comment
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from unicodedata import category

from order_module.models import Order
from product_module.form import ProductCommentForm
from product_module.models import Product, ProductCategory, ProductSubCategory, ProductBrand, ProductComment, \
    ProductImage
from django.db.models import Q, Prefetch, Count ,Avg ,F

from utils.my_decorators import filter_products


class ProductListView(ListView):
    model = Product
    template_name = 'product_module/product_grid.html'
    paginate_by = 24
    context_object_name = "products"
    def get_queryset(self):
        queryset = (Product.objects.filter(
            is_active=True,
            is_deleted=False,
            category__is_active=True
        ).select_related('category','category__main_category' ,'brand')
        .prefetch_related('packs' ,Prefetch('product_image' ,queryset=ProductImage.objects.order_by('-is_Main' ,'id'),to_attr='prefetched_images'))
        .annotate(comments_total=Count('comment_set' ,distinct=True),rating_avarage=Avg('comment_set__rating'))
        .order_by('-chosen','?'))

        category_slug = self.kwargs.get("category")
        subcategory_slug = self.kwargs.get("subcategory")

        if category_slug:
            category = get_object_or_404(ProductCategory,slug=category_slug ,is_active=True)
            if category:
                queryset = queryset.filter(category__main_category=category ,category__is_active=True)
            else:
                return redirect('all_products')

        elif subcategory_slug:
            subcategory = get_object_or_404(ProductSubCategory,slug=subcategory_slug  ,is_active=True)
            if subcategory:
                queryset = queryset.filter(category=subcategory ,category__is_active=True)
            else:
                return redirect('all_products')

        q = self.request.GET.get("q")

        if q:
            queryset = search_product_queryset(q)
            return filter_products(self.request, queryset)

        return filter_products(
            self.request,
            queryset
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs.get("category")
        subcategory_slug = self.kwargs.get("subcategory")
        offer = self.request.GET.get('offer')
        brand = self.request.GET.get('brand')
        brand_grid = self.request.GET.get('brandgrid')
        q = self.request.GET.get('q')

        if category_slug:
            category = ProductCategory.objects.prefetch_related('subcategory').filter(slug=category_slug ,is_active=True).first()
            context["title_prd"] = category.title
            context["current_category"] = category
            context['subcats'] = category.subcategory.filter(is_active=True)

        elif subcategory_slug:
            subcategory = get_object_or_404(
                ProductSubCategory,
                slug=subcategory_slug,
                is_active=True
            )
            context["title_prd"] = subcategory.title
            context["current_category"] = subcategory.main_category
            context["current_subcategory"] = subcategory
            context['subcats'] = ProductSubCategory.objects.filter(main_category=subcategory.main_category ,is_active=True)
        elif q:
            context['title_prd'] = 'نتایج برای ' + q
        elif offer:
            context['title_prd'] = 'تخفیف های ویژه'
        elif brand_grid:
            if brand:
                brand_model = ProductBrand.objects.filter(pk=brand).first()
                context['title_prd'] = f'محصولات {brand_model.title} '
        else:
            context["title_prd"] = "همه محصولات"

        max_price = Product.objects.order_by("-price").first()
        brand = ProductBrand.objects.filter(is_active=True)
        context['brand'] = brand
        context["db_max_price"] = max_price.price if max_price else 0
        context["brands"] = ProductBrand.objects.all()
        context["category_grid"] = ProductCategory.objects.filter(
            is_active=True
        )
        context['selected_brands'] = ProductBrand.objects.filter(id__in=self.request.GET.getlist('brand'))
        context["selected_brands_ids"] = self.request.GET.getlist("brand")
        context["has_filters"] = any([
            self.request.GET.get("order"),
            self.request.GET.get("start_price"),
            self.request.GET.get("end_price"),
            self.request.GET.getlist("brand"),
            self.request.GET.get("available"),
        ])
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_module/Product_details.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_active:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['related_products'] = (Product.objects.filter(
            is_active=True,
            is_deleted=False,
            category__is_active=True,
            quantity__gt=0,
            category__main_category=product.category.main_category
        ).select_related('category','category__main_category' ,'brand')
        .prefetch_related('packs' ,Prefetch('product_image' ,queryset=ProductImage.objects.order_by('-is_Main' ,'id'),to_attr='prefetched_images'))
        .annotate(comments_total=Count('comment_set' ,distinct=True),rating_avarage=Avg('comment_set__rating'))
        .exclude(id=product.id)
        .order_by('-chosen' ,'-quantity'))[:7]

        context['slider_title'] = 'محصولات مرتبط'
        Product.objects.filter(pk=product.pk).update(view=F('view') + 1)
        return context

    def post(self, request, *args, **kwargs):
        message = None
        message_e = None
        self.object = self.get_object()
        product = self.object
        comment_form = ProductCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product

            if request.user.is_authenticated:
                comment.user = request.user
                comment.save()
                message = 'نظر شما بعد از تایید مدیر نمایش داده میشود'
                popup_open = False
            else:
                message_e = 'برای ارسال نظر باید وارد شوید'
                popup_open = True
        else:
            message_e = 'لطفا فیلد متن نظر را پر کنید'
            popup_open = True

        context = self.get_context_data(object=self.object)
        context['message'] = message
        context['message_e'] = message_e
        context['comment_form'] = ProductCommentForm()
        context['popup_open'] = popup_open
        return self.render_to_response(context)

def delete_comment(self ,id):
    try:
        comment = get_object_or_404(ProductComment, id=id)
        if comment:
            comment.delete()
            return redirect('product_detail_page', slug=comment.product.slug)
    except:
        return redirect('home')


def like_comment(request: HttpRequest):
    comment_id = request.GET.get('id')

    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'برای لایک کردن باید وارد شوید',
            'error': True
        })

    comment = ProductComment.objects.get(id=comment_id)

    if not comment:
        return JsonResponse({
            'message': 'کامنت پیدا نشد',
            'error': True
        })

    if request.user in comment.like.all():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)

    html = render_to_string(
        'product_module/product_comment_section.html',
        {
            'product': comment.product,
            'comments': comment,
        },
        request=request
    )

    return JsonResponse({
        'html': html,
        'error': False
    })


def search_product_queryset(q):
    try:
        words = q.split()

        queryset = (Product.objects.filter(
            is_active=True,
            is_deleted=False,
            category__is_active=True
        ).select_related('category','category__main_category' ,'brand')
        .prefetch_related('packs' ,Prefetch('product_image' ,queryset=ProductImage.objects.order_by('-is_Main' ,'id'),to_attr='prefetched_images'))
        .annotate(comments_total=Count('comment_set' ,distinct=True),rating_avarage=Avg('comment_set__rating'))
        .order_by('-chosen' ,'-quantity'))

        for word in words:
            queryset = queryset.filter(
                Q(title__icontains=word) |
                Q(category__title__icontains=word) |
                Q(brand__title__icontains=word)
            )

        return queryset.order_by('-chosen' ,'-quantity')

    except:
        return JsonResponse({
            'message': 'در جستجو مشکلی پیش آمده!',
            'error': True
        })


def search_product(request):
    q = request.GET.get('q', '').strip()

    if len(q) < 2:
        return JsonResponse([], safe=False)

    queryset = search_product_queryset(q)
    products = queryset[:10]

    data = []

    for p in products:
        data.append({
            'title': p.title,
            'price': p.price,
            'offer': p.offer,
            'final_price': p.final_price,
            'url': p.get_absolute_url(),
            'image': p.prefetched_images[0].image.url if p.prefetched_images else ' '
        })


    return JsonResponse({
        'data': data,
        'result_count': queryset.values('id').count()
    }, safe=False)




