from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.ProductListView.as_view() ,name='all_products_page'),
    path('category/<slug:category>/' ,views.ProductListView.as_view() ,name='products_by_category'),
    path('subcategory/<slug:subcategory>/', views.ProductListView.as_view(), name='products_by_subcategory'),
    path('details/<slug:slug>/', views.ProductDetailView.as_view() ,name='product_detail_page'),
    path('details/<int:id>/delete' ,views.delete_comment ,name='comment_delete'),
    path('search/' ,views.search_product ,name='search_products'),
    path('likecomment/' , views.like_comment ,name='like_comment'),

]