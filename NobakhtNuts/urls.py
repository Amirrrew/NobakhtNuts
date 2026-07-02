
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/' ,include('adminpanel_module.url')),
    path('' , include('home_module.url')),
    path('accounts/' ,include('account_module.url')),
    path('userpanel/' ,include('userpanel_module.url')),
    path('support/' ,include('support_module.url')),
    path('products/' ,include('product_module.url')),
    path('orders/' ,include('order_module.url')),
    path('docs/' ,include('documents_module.url')),
    path('articles/' ,include('article_module.url')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
