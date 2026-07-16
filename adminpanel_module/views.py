from itertools import count

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View , ListView, DeleteView, CreateView, UpdateView
import json

from unicodedata import category
from urllib3 import request

from account_module.form import LoginForm
from account_module.models import User , BlackList_phones
from adminpanel_module.forms import ProductAddForm, MainCategoryForm, SubCategoryForm, PackForm, BrandForm, UserForm, \
    SupportWayForm, SiteSettingForm, FooterLinkForm, PaymentForm, CardForm, PostingForm, AdminLoginForm
from order_module.context_processors import orders
from order_module.models import Order, OrderStatus, PaymentMethod, Cards, PostingMethod
from product_module.models import Product, ProductCategory, ProductSubCategory, ProductBrand, PackageSize, \
    ProductFeature, ProductImage, ProductComment
from site_settings.models import SiteSettings, FooterLinkBox, FooterLink
from support_module.models import Ticket, SupportWays
from utils.dashboard_decorators import get_sales_week, get_sales_week_growth, today, get_order_today, get_user_growth, \
    get_new_orders, get_lowstock_products, get_best_selling_products, get_new_tickets, get_sales_month, \
    get_category_chart, get_orders_status_chart, get_orders_month_count
from utils.my_decorators import permision_checker_decorator_factory
from django.db.models import Q, Count ,Sum,Avg


class AdminLogin(LoginView):
    template_name = 'adminpanel_module/auth/admin_login.html'
    authentication_form = AdminLoginForm

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_superuser:
            context = self.get_context_data(form=form)
            context["message_e"] = "شما دسترسی لازم را ندارید"
            return self.render_to_response(context)

        login(self.request, user)
        return redirect('admin_home')

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "نام کاربری یا رمز عبور اشتباه است"
        return self.render_to_response(context)

@permision_checker_decorator_factory({'permission': 'admin_index'})
def logoutPanel(request):
    logout(request)
    return redirect('home')


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def index(request: HttpRequest):
    weeksale = get_sales_week()
    weeksale_growth = get_sales_week_growth()
    users = get_user_growth()
    order_today = get_order_today()
    context = {
        'weeksales': weeksale['max_sale'],
        'weekdayssales': weeksale['days'],
        'total_week_sale': weeksale['total_week_sale'],
        'weeksale_growth': weeksale_growth['percent'],
        'order_count_today': order_today['today_orders'],
        'order_difference': order_today['difference_orders'],
        'today_total': order_today['today_total'],
        'yesterday_total': order_today['yesterday_total'],
        'total_order_growth': order_today['percent'],
        'new_orders': get_new_orders(),
        'all_users': users['all_users'],
        'new_users': users['new_users'],
        'low_stock_products': get_lowstock_products(10),
        'best_selling_products': get_best_selling_products(10),
        # 'new_tickets': get_new_tickets(),
    }
    return render(request, 'adminpanel_module/home/admin_home.html', context)

def admin_sidebar_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_sidebar_component.html', {
        'user': user
    })

def admin_header_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_header_component.html', {
        'user': user
    })

def admin_user_card_component(request):
    context = {
        'new_orders': get_new_orders(),
        'new_tickets': get_new_tickets(),
        'user': request.user,
        'date': today
    }
    return render(request, 'adminpanel_module/shared/components/admin_user_card.html', context)


def admin_popup_user_component(request):
    user = request.user
    return render(request, 'adminpanel_module/shared/components/admin_popup.html', {
        'user': user
    })

def admin_popup_notif_component(request):
    context = {
        'new_orders': get_new_orders(),
        'new_tickets': get_new_tickets(),
        'user': request.user,
    }
    return render(request, 'adminpanel_module/shared/components/admin_popup_notif_component.html', context)

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def StatsHome(request):
    month_data = get_sales_month()
    context = {
        "monthsale": month_data["days"],
        "all_months_sale": month_data["max_sale"],
        "current_month_sale": month_data["total_month_sale"],
        "monthsale_growth": month_data["monthsale_growth"],
    }
    return render(request, 'adminpanel_module/stats/stats_home.html', context)
@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def Products_Stats(request):
    category_data = get_category_chart()
    context = {
        'all_products_count': Product.objects.count,
        'all_available_products': Product.objects.filter(quantity__gte=0).count(),
        'all_unavailable_products': Product.objects.filter(quantity=0).count(),
        'low_stock_products': get_lowstock_products(10),
        'best_selling_products': get_best_selling_products(10),
        'stats_view': True,
        'avarage_price_products': round(Product.objects.aggregate(avg_price=Avg("price"))["avg_price"] or 0),
        'category_data': category_data['categories'],
        'category_max': category_data['max_count']
    }
    return render(request ,'adminpanel_module/stats/products_stats/products_stats.html' ,context)

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def Orders_Stats(request):
    order_status_data = get_orders_status_chart()
    orders_data = get_orders_month_count()
    context = {
        'all_orders': Order.objects.count,
        'status_data': order_status_data['statuses'],
        'status_max': order_status_data['max_count'],
        'avarage_order': int(round((Order.objects.aggregate(avg_price=Avg("finalized_price"))["avg_price"] or 0) ,-3)),
        'attention_needed_orders': Order.objects.filter(Q(status__title='در انتظار تایید') |Q(status__title='پرداخت شده')).count(),
        'month_orders': orders_data['days'],
        'month_orders_max': orders_data['max_orders'],
        'month_total_orders': orders_data['total_orders'],
    }
    return render(request ,'adminpanel_module/stats/orders_stats/orders_stats.html' ,context)


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def Sales_Stats(request):
    period = request.GET.get('period')

    if period == 'week':
        data = get_sales_week()
    elif period == 'month':
        data = get_sales_week()
    elif period == 'year':
        # data = get_sales_year
        pass
    context = {}
    return render(request ,'adminpanel_module/stats/sales_stats/sales_stats.html' ,context)



@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class OrdersListView(ListView):
    model = Order
    template_name = 'adminpanel_module/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 30

    def get_queryset(self):
        search = self.request.GET.get('q')

        queryset = Order.objects.filter(
            is_paid=True
        ).order_by('is_done', '-payment_date' )

        if search:
            if search.isdigit():
                queryset = queryset.filter(
                    Q(pk__icontains=int(search)) |
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )

        return queryset

    def get(self ,request , *args , **kwargs):
        response = super().get(request, *args , **kwargs)
        if request.GET.get('q') is not None:
            html = render_to_string(
                'adminpanel_module/orders/table_components/order_table_partial.html',
                {'orders': self.object_list},
                request=request
            )

            return JsonResponse({
                'html': html,
                'data_length': self.object_list.count() if hasattr(self.object_list, 'count') else len(self.object_list)
            })

        return response

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def OrderDelete(request ,pk):
    order = get_object_or_404(Order, pk=pk)
    if order:
        order.delete()
    return redirect('admin_order_list')

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def OrderSelectedAction(request):
    action = request.GET.get('action')
    orders_ids = request.POST.getlist('order')
    message=None
    if action and orders_ids:
        orders_list = Order.objects.filter(id__in=orders_ids)
        if action == 'delete':
            orders_list.delete()
            message = 'سفارشات با موفقیت حذف شدند'
        elif action == 'approve':
            for order in orders_list:
                order.approve_order()
                message = 'سفارشات تایید شده و در مرحله آماده سازی قرار گرفتند'
        elif action == 'reject':
            for order in orders_list:
                order.reject_order()
                message = 'سفارشات با موفقیت رد شدند'
        elif action == 'send':
            for order in orders_list:
                order.send_order()
                message = 'سفارشات با موفقیت در مرحله ارسال شده قرار گرفتند'

    orders_after = Order.objects.filter(is_paid=True).order_by('is_done', '-payment_date' )
    html = render_to_string(
        'adminpanel_module/orders/table_components/order_table_partial.html',
        {'orders': orders_after},
        request=request
    )

    return JsonResponse({
        'html': html,
        'message': message
    })

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class OrderDetailView(DeleteView):
    model = Order
    template_name = 'adminpanel_module/orders/order_details_admin.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object
        action = request.POST.get('order_action')
        if action == 'approve':
            order.approve_order()
        elif action == 'reject':
            order.reject_order()
        elif action == 'send':
            order.send_order()
        elif action == 'cancel':
            order.return_order()

        return redirect('admin_order_detail' ,pk=order.pk)



@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'adminpanel_module/products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('q')

        queryset = Product.objects.filter(is_deleted=False).order_by('-is_active' ,'-created_at')

        main_category = self.request.GET.get("main_category")
        sub_category = self.request.GET.get("sub_category")

        if main_category:
            queryset = queryset.filter(category__main_category_id=main_category)

        if sub_category:
            queryset = queryset.filter(category_id=sub_category)

        if search:
            if search.isdigit():
                queryset = queryset.filter(
                    Q(pk__icontains=int(search)) |
                    Q(title__icontains=search) |
                    Q(category__title__icontains=search) |
                    Q(category__main_category__title__icontains=search) |
                    Q(brand__title__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(category__title__icontains=search) |
                    Q(category__main_category__title__icontains=search) |
                    Q(brand__title__icontains=search)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = ProductCategory.objects.all()
        context['sub_categories'] = ProductSubCategory.objects.select_related('main_category').all()

        context["selected_main"] = self.request.GET.get("main_category", "")
        context["selected_sub"] = self.request.GET.get("sub_category", "")

        return context

    def get(self ,request , *args , **kwargs):
        response = super().get(request, *args , **kwargs)
        if request.GET.get('q') is not None:
            html = render_to_string(
                'adminpanel_module/products/table_components/product_table_partial.html',
                {'products': self.object_list},
                request=request
            )

            return JsonResponse({
                'html': html,
                'data_length': self.object_list.count() if hasattr(self.object_list, 'count') else len(self.object_list)
            })

        return response


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def ProductSelectedAction(request):
    action = request.GET.get('action')
    product_ids = request.POST.getlist('product')
    message=None
    if action and product_ids:
        product_list = Product.objects.filter(id__in=product_ids)
        if action == 'inactive':
            for product in product_list:
                product.is_active = False
                product.save()
                message = 'کالا های انتخابی غیر فعال شدند'
        if action == 'active':
            for product in product_list:
                if product.price:
                    product.is_active = True
                    product.save()
                    message = 'کالا های انتخابی فعال شدند'
                else:
                    message = 'کالا ها برای فعال شدن باید دارای قیمت باشند'
        if action == 'delete':
            for product in product_list:
                product.is_deleted = True
                product.save()
                message = 'کالا های انتخابی حذف شدند'

    products_after = Product.objects.filter(is_deleted=False)
    html = render_to_string(
        'adminpanel_module/products/table_components/product_table_partial.html',
        {'products': products_after},
        request=request
    )

    return JsonResponse({
        'html': html,
        'message': message
    })

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def ProductDelete(request ,pk):
    product = get_object_or_404(Product, pk=pk)
    if product:
        product.is_deleted = True
        product.save()
    return redirect('admin_product_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class ProductAdd(CreateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'adminpanel_module/products/product_add_update.html'
    success_url = reverse_lazy('admin_product_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        product_features = json.loads(self.request.POST.get('features' ,'[]'))
        for feature in product_features:
            new_feature = ProductFeature(
                title=feature['title'],
                desc=feature['desc'],
                product=self.object,
            )
            new_feature.save()

        images = self.request.FILES.getlist('images')
        for i, img in enumerate(images):
            new_img = ProductImage(
                product=self.object,
                image=img,
                is_Main=(i == 0)
            )
            new_img.save()

        selected_packs = self.request.POST.getlist('packs')
        self.object.packs.set(selected_packs)

        product = self.object
        if not product.price:
            product.is_active = False
            product.save()
        product.user = self.request.user
        product.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self,*args, **kwargs):
        context = super(ProductAdd ,self).get_context_data(*args,**kwargs)
        context['category_options_json'] = json.dumps([
            {'value': c.pk, 'label': c.title, 'parent': c.main_category_id}
            for c in ProductSubCategory.objects.filter(is_active=True)
        ], ensure_ascii=False)

        context['brand_options_json'] = json.dumps([
            {'value': b.pk, 'label': b.title}
            for b in ProductBrand.objects.all()
        ], ensure_ascii=False)
        context['packs'] = PackageSize.objects.all()
        context['add_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class ProductEdit(UpdateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'adminpanel_module/products/product_add_update.html'
    success_url = reverse_lazy('admin_product_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save()

        previous_features = ProductFeature.objects.filter(product=self.object)
        previous_features.delete()
        product_features = json.loads(self.request.POST.get('features' ,'[]'))
        for feature in product_features:
            new_feature = ProductFeature(
                title=feature['title'],
                desc=feature['desc'],
                product=self.object,
            )
            new_feature.save()




        keep_images = json.loads(
            self.request.POST.get("keep_images", "[]")
        )
        ProductImage.objects.filter(product=self.object).exclude(id__in=keep_images).delete()
        images = self.request.FILES.getlist('images')
        for i, img in enumerate(images):
            new_img = ProductImage(
                product=self.object,
                image=img,
                is_Main=(i == 0)
            )
            new_img.save()

        if not ProductImage.objects.filter(
                product=self.object,
                is_Main=True
        ).exists():

            first_image = ProductImage.objects.filter(
                product=self.object
            ).first()

            if first_image:
                first_image.is_Main = True
                first_image.save(update_fields=["is_Main"])

        product = self.object
        if not product.price:
            product.is_active = False
            product.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self,*args, **kwargs):
        context = super(ProductEdit ,self).get_context_data(*args,**kwargs)

        context['category_options_json'] = json.dumps([
            {'value': c.pk, 'label': c.title, 'parent': c.main_category_id}
            for c in ProductSubCategory.objects.filter()
        ], ensure_ascii=False)

        context['brand_options_json'] = json.dumps([
            {'value': b.pk, 'label': b.title}
            for b in ProductBrand.objects.all()
        ], ensure_ascii=False)

        context["product_features"] = json.dumps(
            list(
                self.object.features.values(
                    "id",
                    "title",
                    "desc"
                )
            ),
            ensure_ascii=False
        )

        context["product_images"] = [
            {
                "id": img.id,
                "url": img.image.url,
                "is_cover": img.is_Main,
            }
            for img in self.object.product_image.all()
        ]

        context['selected_packs'] = list(
            self.object.packs.values_list('pk', flat=True)
        )

        context['packs'] = PackageSize.objects.all()
        context['edit_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class MainCategories(ListView):
    model = ProductCategory
    template_name = 'adminpanel_module/categories/categories_list.html'
    context_object_name = 'categories'

    def post(self ,request):
        user = request.user
        password = request.POST.get('password')
        if password and user.check_password(password):
            category = ProductCategory.objects.filter(pk=request.POST.get('cat_pk')).first()
            category.delete()
        return redirect('admin_maincategory_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class MainCategoryAdd(CreateView):
    model = ProductCategory
    form_class = MainCategoryForm
    template_name = 'adminpanel_module/categories/maincategory_add_update.html'
    success_url = reverse_lazy('admin_maincategory_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MainCategoryAdd ,self).get_context_data()
        context['add_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class MainCategoryEdit(UpdateView):
    model = ProductCategory
    form_class = MainCategoryForm
    template_name = 'adminpanel_module/categories/maincategory_add_update.html'
    success_url = reverse_lazy('admin_maincategory_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MainCategoryEdit ,self).get_context_data()
        context['edit_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SubCategories(ListView):
    model = ProductSubCategory
    template_name = 'adminpanel_module/categories/subcategories_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related('subcategory').all()


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SubCategoryAdd(CreateView):
    model = ProductSubCategory
    form_class = SubCategoryForm
    template_name = 'adminpanel_module/categories/subcategories_add_update.html'
    success_url = reverse_lazy('admin_subcategory_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SubCategoryAdd ,self).get_context_data(*args ,**kwargs)
        context['category'] = ProductCategory.objects.all()
        context['add_view'] = True
        return context



@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SubCategoryEdit(UpdateView):
    model = ProductSubCategory
    form_class = SubCategoryForm
    template_name = 'adminpanel_module/categories/subcategories_add_update.html'
    success_url = reverse_lazy('admin_subcategory_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SubCategoryEdit ,self).get_context_data(*args ,**kwargs)
        context['category'] = ProductCategory.objects.all()
        context['edit_view'] = True
        return context

@permision_checker_decorator_factory({'permission': 'admin_index'})
def SubCategoryDelete(request,pk):
    subcat = get_object_or_404(ProductSubCategory,pk=pk)
    if subcat:
        subcat.delete()
    return redirect('admin_subcategory_list')


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class PackList(ListView):
    model = PackageSize
    template_name = 'adminpanel_module/packaging/packs_list.html'
    context_object_name = 'packs'

    def get_queryset(self):
        return PackageSize.objects.all().order_by('size')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class PackAdd(CreateView):
    model = PackageSize
    template_name = 'adminpanel_module/packaging/pack_add_update.html'
    form_class = PackForm
    success_url = reverse_lazy('admin_pack_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(PackAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def PackDelete(request ,pk):
    pack = get_object_or_404(PackageSize ,pk=pk)
    if pack:
        pack.delete()
    return redirect('admin_pack_list')


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class PackEdit(UpdateView):
    model = PackageSize
    template_name = 'adminpanel_module/packaging/pack_add_update.html'
    form_class = PackForm
    success_url = reverse_lazy('admin_pack_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(PackEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class BrandsList(ListView):
    model = ProductBrand
    template_name = 'adminpanel_module/brands/brands_list.html'
    context_object_name = 'brands'

def BrandDelete(request , pk):
    brnd = get_object_or_404(ProductBrand,pk=pk)
    if brnd:
        brnd.delete()
    return redirect('admin_brand_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class BrandAdd(CreateView):
    model = ProductBrand
    template_name = 'adminpanel_module/brands/brand_add_update.html'
    form_class = BrandForm
    success_url = reverse_lazy('admin_brand_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(BrandAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class BrandEdit(UpdateView):
    model = ProductBrand
    template_name = 'adminpanel_module/brands/brand_add_update.html'
    form_class = BrandForm
    success_url = reverse_lazy('admin_brand_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(BrandEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class CommentList(ListView):
    model = ProductComment
    template_name = 'adminpanel_module/comments/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        return ProductComment.objects.filter(is_approved=True).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super(CommentList ,self).get_context_data(*args ,**kwargs)
        context['approval_needed_comments'] = ProductComment.objects.filter(is_approved=False).order_by('-created_at')
        return context

    def get(self,request ,*args, **kwargs):
        comment_pk = request.GET.get('comment')
        comment = ProductComment.objects.filter(pk=comment_pk).first()
        if comment:
            comment.is_approved = True
            comment.save()

            comments = ProductComment.objects.filter(is_approved=True)
            comments_notapproved = ProductComment.objects.filter(is_approved=False)

            html_approved = render_to_string(
                'adminpanel_module/comments/table_components/comments_approved_partial.html',
                {'comments': comments},
                request=request,
            )

            html_notapproved = render_to_string(
                'adminpanel_module/comments/table_components/comments_notapproved_partial.html',
                {'approval_needed_comments': comments_notapproved},
                request=request,
            )
            return JsonResponse({
                'html_a': html_approved,
                'html_na': html_notapproved
            })

        return super().get(request, *args , **kwargs)

@permision_checker_decorator_factory({'permission': 'admin_index'})
def CommentDelete(request , pk):
    comment = get_object_or_404(ProductComment,pk=pk)
    if comment:
        comment.delete()
    return redirect('admin_comment_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class UsersList(ListView):
    model = User
    template_name = 'adminpanel_module/users/users_list.html'
    context_object_name = 'users'
    paginate_by = 30

    def get_queryset(self):
        queryset = User.objects.all().order_by('-is_superuser','-created_at')

        search = self.request.GET.get('q')

        if search:
            if search.isdigit():
                queryset = queryset.filter(
                    Q(pk__icontains=int(search)) |
                    Q(phone__icontains=search) |
                    Q(username__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(phone__icontains=search) |
                    Q(username__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )

        return queryset


    def get(self ,request , *args , **kwargs):
        response = super().get(request, *args , **kwargs)
        if request.GET.get('q') is not None:
            html = render_to_string(
                'adminpanel_module/users/table_components/users_table_partial.html',
                {'users': self.object_list},
                request=request
            )

            return JsonResponse({
                'html': html,
                'data_length': self.object_list.count() if hasattr(self.object_list, 'count') else len(self.object_list)
            })

        return response

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class UserAdd(CreateView):
    model = User
    form_class = UserForm
    template_name = 'adminpanel_module/users/user_add_update.html'
    success_url = reverse_lazy('admin_user_list')
    context_object_name = 'admin_user'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        password = self.request.POST.get('password')
        avatar = self.request.FILES.get('avatar')
        if password:
            self.object.set_password(password)
            self.object.save()
        if avatar:
            self.object.avatar = avatar
            self.object.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(UserAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def UserDelete(request ,pk):
    admin_user = get_object_or_404(User ,pk=pk)
    if admin_user:
        admin_user.delete()
    return redirect('admin_user_list')

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def UserAvatarDelete(request ,pk):
    admin_user = get_object_or_404(User ,pk=pk)
    if admin_user:
        admin_user.avatar.delete()
        admin_user.save()
    return redirect('admin_user_edit' ,pk=pk)

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class UserEdit(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'adminpanel_module/users/user_add_update.html'
    success_url = reverse_lazy('admin_user_list')
    context_object_name = 'admin_user'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        password = self.request.POST.get('password')
        avatar = self.request.FILES.get('avatar')
        if password:
            self.object.set_password(password)
            self.object.save()
        if avatar:
            self.object.avatar = avatar
            self.object.save()


        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(UserEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        context['products_added'] = Product.objects.filter(user=self.object)
        context['orders_commited'] = Order.objects.filter(is_paid=True ,user=self.object)
        context['comments_sent'] = ProductComment.objects.filter(user=self.object)
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class TicketList(ListView):
    model = Ticket
    template_name = 'adminpanel_module/tickets/ticket_list.html'
    context_object_name = 'tickets'


    def get_queryset(self):
        queryset = Ticket.objects.all().order_by('-created_at' ,'status')
        print(settings.TIME_ZONE)
        print(settings.USE_TZ)
        print(timezone.now())
        print(timezone.localtime())

        search = self.request.GET.get('q')

        if search:
            if search.isdigit():
                queryset = queryset.filter(
                    Q(pk__icontains=int(search)) |
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )
            else:
                queryset = queryset.filter(
                    Q(user__phone__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search)
                )

        return queryset


    def get(self ,request , *args , **kwargs):
        response = super().get(request, *args , **kwargs)
        if request.GET.get('q') is not None:
            html = render_to_string(
                'adminpanel_module/tickets/table_components/ticket_table_partial.html',
                {'tickets': self.object_list},
                request=request
            )

            return JsonResponse({
                'html': html,
                'data_length': self.object_list.count() if hasattr(self.object_list, 'count') else len(self.object_list)
            })

        return response

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SupportWays_list(ListView):
    model = SupportWays
    template_name = 'adminpanel_module/support_ways/supportways_list.html'
    context_object_name = 'supportways'

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def SupportWayDelete(request ,pk):
    sw = get_object_or_404(SupportWays,pk=pk)
    if sw:
        sw.delete()
    return redirect('admin_supportways_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SupportWayAdd(CreateView):
    model = SupportWays
    template_name = 'adminpanel_module/support_ways/supportway_add_update.html'
    form_class = SupportWayForm
    success_url = reverse_lazy('admin_supportways_list')
    context_object_name = 'supportway'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SupportWayAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SupportWayEdit(UpdateView):
    model = SupportWays
    template_name = 'adminpanel_module/support_ways/supportway_add_update.html'
    form_class = SupportWayForm
    success_url = reverse_lazy('admin_supportways_list')
    context_object_name = 'supportway'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SupportWayEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SiteSettingsList(ListView):
    model = SiteSettings
    template_name = 'adminpanel_module/settings/settings_list.html'
    context_object_name = 'sitesettings'

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SiteSettingsAdd(CreateView):
    model = SiteSettings
    form_class = SiteSettingForm
    template_name = 'adminpanel_module/settings/settings_add_update.html'
    success_url = reverse_lazy('admin_sitesettings_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        is_default = self.request.POST.get('is_default')
        if is_default:
            all_settings = SiteSettings.objects.filter(is_default=True)
            for s in all_settings:
                s.is_default = False
            self.object.is_default = True
            self.object.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SiteSettingsAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class SiteSettingsEdit(UpdateView):
    model = SiteSettings
    form_class = SiteSettingForm
    template_name = 'adminpanel_module/settings/settings_add_update.html'
    success_url = reverse_lazy('admin_sitesettings_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        is_default = self.request.POST.get('is_default')
        if is_default:
            all_settings = SiteSettings.objects.all()
            for s in all_settings:
                s.is_default = False
            self.object.is_default = True
            self.object.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(SiteSettingsEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class FooterLinkList(ListView):
    model = FooterLinkBox
    template_name = 'adminpanel_module/footerlinks/footerlink_list.html'
    context_object_name = 'footerlinks'

    def get_queryset(self):
        return FooterLinkBox.objects.prefetch_related('links').all()

    def get(self,request ,*args, **kwargs):
        response = super().get(request, *args , **kwargs)
        title = request.GET.get('title')
        if title:
            new_footer_box = FooterLinkBox(
                title=title,
            )
            new_footer_box.save()
            all_footers = FooterLinkBox.objects.prefetch_related('links').all()
            html = render_to_string(
                'adminpanel_module/footerlinks/footerlink_partial.html',
                {'footerlinks': all_footers},
                request=request,
            )
            return JsonResponse({
                'html': html
            })
        return response

@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def FooterBoxDelete(request ,pk):
    fb = get_object_or_404(FooterLinkBox ,pk=pk)
    if fb:
        fb.delete()
    return redirect('admin_footerlinks_list')

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class FooterLinkAdd(CreateView):
    model = FooterLink
    template_name = 'adminpanel_module/footerlinks/footerlink_add_update.html'
    form_class = FooterLinkForm
    success_url = reverse_lazy('admin_footerlinks_list')
    context_object_name = 'footerlink'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(FooterLinkAdd ,self).get_context_data(*args ,**kwargs)
        context['footerboxes'] = FooterLinkBox.objects.all()
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['add_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class FooterLinkEdit(UpdateView):
    model = FooterLink
    template_name = 'adminpanel_module/footerlinks/footerlink_add_update.html'
    form_class = FooterLinkForm
    success_url = reverse_lazy('admin_footerlinks_list')
    context_object_name = 'footerlink'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(FooterLinkEdit ,self).get_context_data(*args ,**kwargs)
        context['footerboxes'] = FooterLinkBox.objects.all()
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['edit_view'] = True
        return context


@permision_checker_decorator_factory({'permission': 'admin_index'} ,)
def FooterLinkDelete(request ,pk):
    fl = get_object_or_404(FooterLink ,pk=pk)
    if fl:
        fl.delete()
    return redirect('admin_footerlinks_list')


@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class PaymentList(ListView):
    model = PaymentMethod
    template_name = 'adminpanel_module/payment_settings/payment_list.html'
    context_object_name = 'payment_settings'

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class PaymentEdit(UpdateView):
    model = PaymentMethod
    form_class = PaymentForm
    template_name = 'adminpanel_module/payment_settings/payment_update.html'
    context_object_name = 'payment_settings'
    success_url = reverse_lazy('admin_payment_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(PaymentEdit ,self).get_context_data(*args ,**kwargs)
        context['cards'] = Cards.objects.all()
        return context



@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class CardsList(ListView):
    model = Cards
    template_name = 'adminpanel_module/my_cards/cards_list.html'
    context_object_name = 'cards'

@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class CardAdd(CreateView):
    model = Cards
    template_name = 'adminpanel_module/my_cards/card_add_update.html'
    context_object_name = 'card'
    success_url = reverse_lazy('admin_cards_list')
    form_class = CardForm


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(CardAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class CardEdit(UpdateView):
    model = Cards
    template_name = 'adminpanel_module/my_cards/card_add_update.html'
    context_object_name = 'card'
    success_url = reverse_lazy('admin_cards_list')
    form_class = CardForm


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(CardEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context

@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class PostingList(ListView):
    model = PostingMethod
    template_name = 'adminpanel_module/posting_fees/postings_list.html'
    context_object_name = 'posting'


@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class PostingAdd(CreateView):
    model = PostingMethod
    template_name = 'adminpanel_module/posting_fees/posting_add_update.html'
    context_object_name = 'posting'
    success_url = reverse_lazy('admin_posting_list')
    form_class = PostingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(PostingAdd ,self).get_context_data(*args ,**kwargs)
        context['add_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class PostingEdit(UpdateView):
    model = PostingMethod
    template_name = 'adminpanel_module/posting_fees/posting_add_update.html'
    context_object_name = 'posting'
    success_url = reverse_lazy('admin_posting_list')
    form_class = PostingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["message_e"] = "فیلد هارا به درستی پر کنید"
        return self.render_to_response(context)

    def get_context_data(self, *args,**kwargs):
        context = super(PostingEdit ,self).get_context_data(*args ,**kwargs)
        context['edit_view'] = True
        return context


@method_decorator(permision_checker_decorator_factory() ,name='dispatch')
class BlackList_list(ListView):
    model = BlackList_phones
    template_name = 'adminpanel_module/blacklist/blacklist.html'
    context_object_name = 'blacklist'

    def get_queryset(self):
        return BlackList_phones.objects.all()

    def get(self,request ,*args, **kwargs):
        phone = request.GET.get('phone')
        if phone:
            new_banned_number = BlackList_phones(
                phone=phone,
            )
            new_banned_number.save()
            blacklist = BlackList_phones.objects.all()
            html = render_to_string(
                'adminpanel_module/blacklist/blacklist_partial.html',
                {'blacklist': blacklist},
                request=request,
            )
            return JsonResponse({
                'html': html
            })

        return super().get(request, *args , **kwargs)

@permision_checker_decorator_factory({'permission': 'admin_index'})
def BlackList_delete(request ,pk):
    phone = get_object_or_404(BlackList_phones ,pk=pk)
    if phone:
        phone.delete()
    return redirect('admin_blacklist')