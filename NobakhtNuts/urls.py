
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

from NobakhtNuts.sitemap import StaticViewSitemap
from article_module.sitemaps import ArticleSitemap
from home_module.views import ServiceWorkerView
from product_module.sitemaps import ProductSitemap, CategorySitemap, SubCategorySitemap

handler404 = 'home_module.views.not_found'

sitemaps = {
    'home': StaticViewSitemap,
    'products': ProductSitemap,
    'category': CategorySitemap,
    'sub_category': SubCategorySitemap,
    'articles': ArticleSitemap
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps ,'template_name': 'sitemap/custom_sitemap.xml'}, name='sitemap'),
    path('admin-nbnadmin-586187/', admin.site.urls),
    path('adminpanel/' ,include('adminpanel_module.url')),
    path('' , include('home_module.url')),
    path('accounts/' ,include('account_module.url')),
    path('userpanel/' ,include('userpanel_module.url')),
    path('support/' ,include('support_module.url')),
    path('products/' ,include('product_module.url')),
    path('orders/' ,include('order_module.url')),
    path('docs/' ,include('documents_module.url')),
    path('articles/' ,include('article_module.url')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(
        "service-worker.js",
        ServiceWorkerView.as_view(),
        name="service_worker",
    ),
]