from itertools import count

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
import json
from adminpanel_module.forms import ProductAddForm
from order_module.context_processors import orders
from order_module.models import Order, OrderStatus
from product_module.models import Product, ProductCategory, ProductSubCategory, ProductBrand, PackageSize, \
    ProductFeature
from utils.dashboard_decorators import get_sales_week, get_sales_week_growth, today, get_order_today, get_user_growth, \
    get_new_orders, get_lowstock_products, get_best_selling_products, get_new_tickets
from utils.my_decorators import permision_checker_decorator_factory
from django.db.models import Q


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
        'low_stock_products': get_lowstock_products(),
        'best_selling_products': get_best_selling_products(),
        'new_tickets': get_new_tickets(),
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

@method_decorator(permision_checker_decorator_factory(), name='dispatch')
class OrdersListView(ListView):
    model = Order
    template_name = 'adminpanel_module/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

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
                product.is_active = True
                product.save()
                message = 'کالا های انتخابی فعال شدند'
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


class ProductAdd(CreateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'adminpanel_module/products/product_add_update.html'
    success_url = reverse_lazy('admin_product_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

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


class ProductEdit(UpdateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'adminpanel_module/products/product_add_update.html'

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

        context['packs'] = PackageSize.objects.all()
        context['add_view'] = True
        return context


