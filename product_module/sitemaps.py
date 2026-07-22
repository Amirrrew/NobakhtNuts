from django.contrib.sitemaps import Sitemap
from .models import Product, ProductCategory, ProductSubCategory


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(
            is_active=True,
            is_deleted=False
        )

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        return 1.0 if obj.chosen else 0.8


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ProductCategory.objects.filter(
            is_active=True
        )

    def location(self, obj):
        return obj.get_absolute_url()

class SubCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ProductSubCategory.objects.filter(
            is_active=True
        )

    def location(self, obj):
        return obj.get_absolute_url()